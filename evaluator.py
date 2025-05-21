from tokens import Token

class Evaluator:
    def __init__(self):
        self.variables = {}  # Store variable names and their values

    def evaluate(self, ast):
        return self._eval(ast)

    @staticmethod
    def _are_compatible(a, b, operator):
        if operator == 'PLUS':
            return (isinstance(a, (int, float)) and isinstance(b, (int, float))) or \
                   (isinstance(a, str) and isinstance(b, str))
        elif operator in ('MINUS', 'MUL', 'DIV'):
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        elif operator in ('AND', 'OR'):
            return isinstance(a, bool) and isinstance(b, bool)
        elif operator in ('EQ', 'NEQ'):
            return type(a) == type(b)
        elif operator in ('LT', 'GT', 'LTE', 'GTE'):
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        else:
            return True

    def _eval(self, node):
        if isinstance(node, Token):
            if node.type == 'IDENT':
                var_name = node.value
                if var_name in self.variables:
                    return self.variables[var_name]
                else:
                    raise ValueError(f"Unknown identifier: {var_name}")
            return node.value

        if isinstance(node, tuple):
            if node[0] == 'PRINT':
                expr = node[1]
                value = self._eval(expr)
                print(value)
                return None

            if node[0] == 'ASSIGN':
                var_token = node[1]
                expr = node[2]
                value = self._eval(expr)
                self.variables[var_token.value] = value
                return value

            op, left, right = node

            if op.type == 'MINUS' and left is None:
                val = self._eval(right)
                if not isinstance(val, (int, float)):
                    raise TypeError(f"Cannot negate non-number: {val}")
                return -val

            if op.type == 'NOT':
                operand = self._eval(right)
                if not isinstance(operand, bool):
                    raise TypeError(f"Cannot apply NOT to non-boolean: {operand}")
                return not operand

            left_val = self._eval(left) if left else None
            right_val = self._eval(right)

            if op.type in ('PLUS', 'MINUS', 'MUL', 'DIV', 'AND', 'OR', 'EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE'):
                if not self._are_compatible(left_val, right_val, op.type):
                    raise TypeError(
                        f"Unsupported operand types: {type(left_val)} and {type(right_val)} for operator {op.type}"
                    )

            if op.type == 'PLUS':
                return left_val + right_val
            elif op.type == 'MINUS':
                return left_val - right_val
            elif op.type == 'MUL':
                return left_val * right_val
            elif op.type == 'DIV':
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero")
                return left_val / right_val
            elif op.type == 'EQ':
                return left_val == right_val
            elif op.type == 'NEQ':
                return left_val != right_val
            elif op.type == 'LT':
                return left_val < right_val
            elif op.type == 'GT':
                return left_val > right_val
            elif op.type == 'LTE':
                return left_val <= right_val
            elif op.type == 'GTE':
                return left_val >= right_val
            elif op.type == 'AND':
                return left_val and right_val
            elif op.type == 'OR':
                return left_val or right_val

        raise Exception(f"Unknown node: {node}")
