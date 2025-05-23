from tokens import Token
from scanner import Scanner
from parser import Parser
from data import Data  # variable storage class

class VariableNotDefinedError(NameError):
    pass

class TypeConversionError(TypeError):
    pass

class Evaluator:
    def __init__(self):
        self.data = Data()  # Variable storage

    def evaluate(self, ast):
        return self._eval(ast)

    @staticmethod
    def _are_compatible(a, b, operator):
        if operator == 'PLUS':
            # Allow only same-type or numeric + numeric
            if isinstance(a, str) and isinstance(b, str):
                return True
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return True
            return False

        elif operator in ('MINUS', 'MUL', 'DIV'):
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        elif operator in ('AND', 'OR'):
            return isinstance(a, bool) and isinstance(b, bool)
        elif operator in ('EQ', 'NEQ'):
            return True
        elif operator in ('LT', 'GT', 'LTE', 'GTE'):
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        else:
            return True

    def _eval(self, node):
        if isinstance(node, Token):
            if node.type == 'VARIABLE':
                try:
                    return self.data.read(node)
                except KeyError:
                    raise VariableNotDefinedError(f"Variable '{node.value}' is not defined.")
            return node.value

        if isinstance(node, tuple):
            tag = node[0]

            if tag == 'BLOCK':
                result = None
                for stmt in node[1]:
                    result = self._eval(stmt)
                return result

            if tag == 'ASSIGN':
                var_token = node[1]
                expr = node[2]
                value = self._eval(expr)
                self.data.write(var_token, value)
                return None

            if tag == 'PRINT':
                expr = node[1]
                value = self._eval(expr)
                print(value)
                return None

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

            if tag == 'WHILE':
                condition = node[1]
                action = node[2]
                result = None
                while self._eval(condition):
                    result = self._eval(action)
                return result

            if tag == 'DEL':
                var_token = node[1]
                self.data.delete(var_token)
                return None

            if len(node) == 3:
                op, left, right = node
                op_type = op.type if isinstance(op, Token) else op

                if op_type == 'MINUS' and left is None:
                    val = self._eval(right)
                    if not isinstance(val, (int, float)):
                        raise TypeConversionError(f"Cannot negate non-number: {val}")
                    return -val

                if op_type == 'NOT' and left is None:
                    operand = self._eval(right)
                    if not isinstance(operand, bool):
                        raise TypeConversionError(f"Cannot apply NOT to non-boolean: {operand}")
                    return not operand

                left_val = self._eval(left) if left is not None else None
                right_val = self._eval(right)

                if op_type in ('PLUS', 'MINUS', 'MUL', 'DIV', 'AND', 'OR', 'LT', 'GT', 'LTE', 'GTE'):
                    if not self._are_compatible(left_val, right_val, op_type):
                        raise TypeConversionError(
                            f"Unsupported operand types: {type(left_val).__name__} and {type(right_val).__name__} for operator {op_type}"
                        )

                if op_type == 'PLUS':
                    return left_val + right_val
                elif op_type == 'MINUS':
                    return left_val - right_val
                elif op_type == 'MUL':
                    return left_val * right_val
                elif op_type == 'DIV':
                    if right_val == 0:
                        raise ZeroDivisionError("Division by zero")
                    return left_val / right_val
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

        raise Exception(f"Unknown AST node encountered: {node}")

# Single instance of evaluator
evaluator_instance = Evaluator()

def evaluate(expression: str):
    scanner = Scanner(expression)
    parser = Parser(scanner)
    ast = parser.parse()
    return evaluator_instance.evaluate(ast)
