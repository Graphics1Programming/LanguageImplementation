from tokens import Token
from scanner import Scanner
from parser import Parser
from data import Data  # variable storage class

# Custom exception for undefined variable access
class VariableNotDefinedError(NameError):
    pass

# Custom exception for type conversion errors during evaluation
class TypeConversionError(TypeError):
    pass

class Evaluator:
    def __init__(self):
        # Data instance to hold variables and their values
        self.data = Data()

    def evaluate(self, ast):
        # Public method to start evaluation of the AST
        return self._eval(ast)

    @staticmethod
    def _are_compatible(a, b, operator):
        """
        Check if operands a and b are compatible for the given operator.
        Rules differ based on operator type (e.g., PLUS allows strings or numbers).
        """
        if operator == 'PLUS':
            # Allow if either operand is string, allow coercion to string
            if isinstance(a, str) or isinstance(b, str):
                return True
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return True
            return False
        elif operator in ('MINUS', 'MUL', 'DIV'):
            # Numeric operations require both operands to be numbers
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        elif operator == 'MOD':
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        elif operator in ('AND', 'OR'):
            # Logical operations require boolean operands
            return isinstance(a, bool) and isinstance(b, bool)
        elif operator in ('EQ', 'NEQ'):
            # Equality operators allow all types
            return True
        elif operator in ('LT', 'GT', 'LTE', 'GTE'):
            # Comparison operators require numeric operands
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        else:
            # Default to True for unknown operators (flexible)
            return True

    def _eval(self, node):
        """
        Recursively evaluate an AST node.
        - Handles tokens (variables/constants)
        - Handles tuples representing AST structures like BLOCK, ASSIGN, IF, WHILE, etc.
        """
        if isinstance(node, Token):
            # If node is a variable, retrieve its value from storage
            if node.type == 'VARIABLE':
                try:
                    return self.data.read(node)
                except KeyError:
                    raise VariableNotDefinedError(f"Variable '{node.value}' is not defined.")
            # For literals, just return their value
            return node.value

        if isinstance(node, tuple):
            tag = node[0]

            if tag == 'INT_CAST':
                expr = node[1]
                val = self._eval(expr)
                try:
                    return int(val)
                except (ValueError, TypeError) as e:
                    raise TypeConversionError(f"Cannot cast value {val} to int: {e}")

            # Evaluate a block of statements sequentially, return last result
            if tag == 'BLOCK':
                result = None
                for stmt in node[1]:
                    result = self._eval(stmt)
                return result

            # Handle variable assignment: evaluate expression, store in variable
            if tag == 'ASSIGN':
                var_token = node[1]
                expr = node[2]
                value = self._eval(expr)
                self.data.write(var_token, value)
                return None

            # Handle print statement: evaluate expression and output it
            if tag == 'PRINT':
                expr = node[1]
                value = self._eval(expr)
                print(value)
                return None

            # Handle input statement: read input from user with prompt
            if tag == 'INPUT':
                prompt_expr = node[1]
                prompt_value = self._eval(prompt_expr)
                return input(str(prompt_value))

            # Handle if-elif-else control flow
            if tag == 'IF':
                conditions = node[1]
                actions = node[2]
                else_action = node[3]
                for cond, action in zip(conditions, actions):
                    if self._eval(cond):
                        return self._eval(action)
                if else_action:
                    return self._eval(else_action)
                return None

            # Handle while loop: repeatedly evaluate action while condition is true
            if tag == 'WHILE':
                condition = node[1]
                action = node[2]
                result = None
                while self._eval(condition):
                    result = self._eval(action)
                return result

            # Handle deletion of variables
            if tag == 'DEL':
                var_token = node[1]
                self.data.delete(var_token)
                return None

            # Handle binary and unary operations with two or three tuple elements
            if len(node) == 3:
                op, left, right = node
                op_type = op.type if isinstance(op, Token) else op

                # Unary minus (negation)
                if op_type == 'MINUS' and left is None:
                    val = self._eval(right)
                    if not isinstance(val, (int, float)):
                        raise TypeConversionError(f"Cannot negate non-number: {val}")
                    return -val

                # Unary NOT operation
                if op_type == 'NOT' and left is None:
                    operand = self._eval(right)
                    if not isinstance(operand, bool):
                        raise TypeConversionError(f"Cannot apply NOT to non-boolean: {operand}")
                    return not operand

                # Evaluate operands for binary operations
                left_val = self._eval(left) if left is not None else None
                right_val = self._eval(right)

                # Check operand compatibility for operators
                if op_type in ('PLUS', 'MINUS', 'MUL', 'DIV', 'AND', 'OR', 'LT', 'GT', 'LTE', 'GTE'):
                    if not self._are_compatible(left_val, right_val, op_type):
                        raise TypeConversionError(
                            f"Unsupported operand types: {type(left_val).__name__} and {type(right_val).__name__} for operator {op_type}"
                        )

                # Perform the actual operation based on operator type
                if op_type == 'PLUS':
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
                        raise ZeroDivisionError("Division by zero in modulus operation")
                    return left_val % right_val
                elif op_type == 'EQ':
                    # Equality: different types always return False
                    if type(left_val) != type(right_val):
                        return False
                    return left_val == right_val
                elif op_type == 'NEQ':
                    # Inequality: different types always return True
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

        # If node structure is not recognised, raise an error
        raise Exception(f"Unknown AST node encountered: {node}")

# Create a single global instance of Evaluator for reuse
evaluator_instance = Evaluator()

def evaluate(expression: str):
    """
    Convenience function to evaluate a string expression:
    1. Scan tokens
    2. Parse into AST
    3. Evaluate AST
    """
    scanner = Scanner(expression)
    parser = Parser(scanner)
    ast = parser.parse()
    return evaluator_instance.evaluate(ast)
