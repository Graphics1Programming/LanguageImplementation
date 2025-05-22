from tokens import Token
from scanner import Scanner
from parser import Parser
from data import Data  # Your variable storage class

class Evaluator:
    def __init__(self):
        self.data = Data()  # Variable storage

    def evaluate(self, ast):
        return self._eval(ast)

    @staticmethod
    def _are_compatible(a, b, operator):
        if operator == 'PLUS':
            # Do not allow None operands for PLUS
            if a is None or b is None:
                return False

            # Strict typing for PLUS:
            # Allow number + number or string + string only
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return True
            if isinstance(a, str) and isinstance(b, str):
                return True

            # Otherwise (e.g., number + string or string + number) not allowed
            return False

        elif operator in ('MINUS', 'MUL', 'DIV'):
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        elif operator in ('AND', 'OR'):
            return isinstance(a, bool) and isinstance(b, bool)
        elif operator in ('EQ', 'NEQ'):
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return True
            return type(a) == type(b)
        elif operator in ('LT', 'GT', 'LTE', 'GTE'):
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        else:
            return True  # Default: no strict checks

    def _eval(self, node):
        # If node is a Token
        if isinstance(node, Token):
            if node.type == 'VARIABLE':
                try:
                    return self.data.read(node)
                except KeyError:
                    raise NameError(f"Variable '{node.value}' is not defined.")
            return node.value

        # If node is a tuple (AST node)
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

            # For operation nodes: assume form (operator, left, right)
            if len(node) == 3:
                op, left, right = node

                # op can be a Token or string; unify:
                op_type = op.type if isinstance(op, Token) else op

                # Unary operators: left is None
                if op_type == 'MINUS' and left is None:
                    val = self._eval(right)
                    if not isinstance(val, (int, float)):
                        raise TypeError(f"Cannot negate non-number: {val}")
                    return -val

                if op_type == 'NOT' and left is None:
                    operand = self._eval(right)
                    if not isinstance(operand, bool):
                        raise TypeError(f"Cannot apply NOT to non-boolean: {operand}")
                    return not operand

                left_val = self._eval(left) if left is not None else None
                right_val = self._eval(right)

                if op_type in ('PLUS', 'MINUS', 'MUL', 'DIV', 'AND', 'OR', 'EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE'):
                    if not self._are_compatible(left_val, right_val, op_type):
                        raise TypeError(
                            f"Unsupported operand types: {type(left_val).__name__} and {type(right_val).__name__} for operator {op_type}"
                        )

                # Evaluate binary operations
                if op_type == 'PLUS':
                    if left_val is None or right_val is None:
                        raise TypeError(f"Cannot add NoneType operands: {left_val} + {right_val}")

                    # Only allow string+string or number+number (enforced above)
                    if isinstance(left_val, str) and isinstance(right_val, str):
                        return left_val + right_val
                    else:
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
                    return left_val == right_val
                elif op_type == 'NEQ':
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


# Single instance of evaluator for reuse
evaluator_instance = Evaluator()


def evaluate(expression: str):
    scanner = Scanner(expression)
    parser = Parser(scanner)
    ast = parser.parse()
    return evaluator_instance.evaluate(ast)
