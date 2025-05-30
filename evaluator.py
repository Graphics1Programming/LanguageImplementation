"""
Evaluator module for executing parsed abstract syntax trees (AST).
Handles expression evaluation, control flow (if/while), assignments,
and built-in operations like input/output, deletion, and type casting.
"""

from tokens import Token
from scanner import Scanner
from parser import Parser
from data import Data, List



class VariableNotDefinedError(NameError):
    """Raised when an undefined variable is accessed."""
    pass


class TypeConversionError(TypeError):
    """Raised when type conversion fails during evaluation."""
    pass


class BreakException(Exception):
    """Used to break out of a while loop."""
    pass

class ContinueException(Exception):
    pass


class Evaluator:
    """
    Evaluates an abstract syntax tree (AST) produced by the parser.
    Supports variables, arithmetic, logical operations, and control structures.
    """

    def __init__(self):
        self.data = Data()  # Stores variable names and values

    def evaluate(self, ast):
        """Public method to evaluate an AST."""
        return self._eval(ast)

    @staticmethod
    def _are_compatible(a, b, operator):
        """
        Check type compatibility for binary operations.
        """
        if operator == 'PLUS':
            # Allow concatenation of two Lists
            if isinstance(a, List) and isinstance(b, List):
                return True
            if isinstance(a, str) or isinstance(b, str):
                return True
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        elif operator in ('MINUS', 'MUL', 'DIV', 'MOD'):
            # Disallow list with other types here
            if isinstance(a, List) or isinstance(b, List):
                return False
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        elif operator in ('AND', 'OR'):
            return isinstance(a, bool) and isinstance(b, bool)
        elif operator in ('EQ', 'NEQ'):
            return True  # allow any types for == and !=
        elif operator in ('LT', 'GT', 'LTE', 'GTE'):
            # Do not support comparison of Lists with numbers or other types here
            if isinstance(a, List) or isinstance(b, List):
                return False
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        return True

    def _eval(self, node):
        """
        Core recursive method to evaluate AST nodes.
        Supports control flow, expressions, assignment, and IO.
        """
        if isinstance(node, Token):
            if node.type == 'VARIABLE':
                try:
                    return self.data.read(node)
                except KeyError:
                    raise VariableNotDefinedError(f"Variable '{node.value}' is not defined.")
            return node.value

        if isinstance(node, tuple):
            tag = node[0]

            if tag == 'INT_CAST':
                val = self._eval(node[1])
                try:
                    return int(val)
                except (ValueError, TypeError) as e:
                    raise TypeConversionError(f"Cannot cast to int: {e}")
            if tag == 'LIST_LITERAL':
                elements = [self._eval(elem) for elem in node[1]]
                return List(elements)

            if tag == 'LIST_ACCESS':
                list_obj = self._eval(node[1])
                if not isinstance(list_obj, List):
                    raise TypeError("LIST_ACCESS requires a List object")
                index = self._eval(node[2])
                if not isinstance(index, int):
                    raise TypeError("List index must be an integer")
                return list_obj.get(index)

            if tag == 'LIST_APPEND':
                list_obj = self._eval(node[1])
                if not isinstance(list_obj, List):
                    raise TypeError("LIST_APPEND requires a List object")
                value = self._eval(node[2])
                list_obj.append(value)
                return None

            if tag == 'LIST_REMOVE':
                list_obj = self._eval(node[1])
                if not isinstance(list_obj, List):
                    raise TypeError("LIST_REMOVE requires a List object")
                index = self._eval(node[2])
                if not isinstance(index, int):
                    raise TypeError("List remove index must be an integer")
                return list_obj.remove(index)

            if tag == 'METHOD_CALL':
                obj = self._eval(node[1])
                method_token = node[2]
                args_nodes = node[3]

                method_name = method_token.value
                args = [self._eval(arg) for arg in args_nodes]

                method = getattr(obj, method_name, None)
                if method is None or not callable(method):
                    raise TypeError(f"Object of type {type(obj).__name__} has no method '{method_name}'")

                return method(*args)

            if tag == 'BLOCK':
                result = None
                for stmt in node[1]:
                    result = self._eval(stmt)
                return result

            if tag == 'ASSIGN':
                value = self._eval(node[2])
                self.data.write(node[1], value)
                return None

            if tag == 'PRINT':
                value = self._eval(node[1])
                print(value)
                return None

            if tag == 'INPUT':
                prompt_value = self._eval(node[1])
                return input(str(prompt_value))

            if tag == 'IF':
                for cond, action in zip(node[1], node[2]):
                    if self._eval(cond):
                        return self._eval(action)
                if node[3]:
                    return self._eval(node[3])
                return None

            if tag == 'WHILE':
                result = None
                while self._eval(node[1]):
                    try:
                        result = self._eval(node[2])
                    except BreakException:
                        break
                    except ContinueException:
                        continue
                return result

            if tag == 'DEL':
                self.data.delete(node[1])
                return None

            if tag == 'BREAK':
                raise BreakException()
            elif tag == 'CONTINUE':
                raise ContinueException()

            if len(node) == 3:
                op, left, right = node
                op_type = op.type if isinstance(op, Token) else op

                if op_type == 'MINUS' and left is None:
                    val = self._eval(right)
                    if not isinstance(val, (int, float)):
                        raise TypeConversionError("Unary minus requires a number")
                    return -val

                if op_type == 'NOT' and left is None:
                    operand = self._eval(right)
                    if not isinstance(operand, bool):
                        raise TypeConversionError("Unary NOT requires a boolean")
                    return not operand

                left_val = self._eval(left) if left is not None else None
                right_val = self._eval(right)

                if not self._are_compatible(left_val, right_val, op_type):
                    raise TypeConversionError(
                        f"Incompatible types: {type(left_val).__name__} and {type(right_val).__name__} for {op_type}"
                    )

                # Binary operation handling
                if op_type == 'PLUS':
                    if isinstance(left_val, List) and isinstance(right_val, List):
                        # Return a new List with combined elements
                        return List(left_val.elements + right_val.elements)
                    if isinstance(left_val, str) or isinstance(right_val, str):
                        return str(left_val) + str(right_val)
                    return left_val + right_val

                elif op_type == 'MINUS':
                    return left_val - right_val
                elif op_type == 'MUL':
                    return left_val * right_val
                elif op_type == 'DIV':
                    if right_val == 0:
                        raise ZeroDivisionError("Division by zero")
                    return left_val / right_val
                elif op_type == 'MOD':
                    if right_val == 0:
                        raise ZeroDivisionError("Modulus by zero")
                    return left_val % right_val
                elif op_type == 'EQ':
                    if type(left_val) != type(right_val):
                        return False
                    return left_val == right_val
                elif op_type == 'NEQ':
                    if type(left_val) != type(right_val):
                        return True
                    return left_val != right_val
                elif op_type == 'LT':
                    return left_val < right_val
                elif op_type == 'GT':
                    return left_val > right_val
                elif op_type == 'LTE':
                    return left_val <= right_val
                elif op_type == 'GTE':
                    return left_val >= right_val
                elif op_type == 'AND':
                    return left_val and right_val
                elif op_type == 'OR':
                    return left_val or right_val

        raise Exception(f"Unknown AST node: {node}")


# Global Evaluator instance
evaluator_instance = Evaluator()


def evaluate(expression: str):
    """
    Evaluate an input expression string by:
    1. Scanning into tokens
    2. Parsing into an AST
    3. Evaluating the AST
    """
    scanner = Scanner(expression)
    parser = Parser(scanner)
    ast = parser.parse()
    return evaluator_instance.evaluate(ast)
