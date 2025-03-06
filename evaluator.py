from tokens import Token

class Evaluator:
    def evaluate(self, ast):
        return self._eval(ast)

    def _are_compatible(self, a, b, allow_number_bool=False):
        """Check if two values are compatible for an operation."""
        # Explicitly exclude booleans from being treated as numbers
        def is_number(x):
            return type(x) in (int, float)  # Use type() instead of isinstance()

        def is_bool(x):
            return type(x) is bool

        if allow_number_bool:
            return (is_number(a) or is_bool(a)) and (is_number(b) or is_bool(b))
        else:
            return is_number(a) and is_number(b)

    def _eval(self, node):
        if isinstance(node, Token):
            return node.value

        if isinstance(node, tuple):
            op, left, right = node

            # Handle unary negation (e.g., "-5")
            if op.type == 'MINUS' and left is None:
                val = self._eval(right)
                if not isinstance(val, (int, float)):
                    raise TypeError(f"Cannot negate non-number: {val}")
                return -val

            # Handle logical NOT ("not true")
            if op.type == 'NOT':
                operand = self._eval(right)
                if type(operand) is not bool:
                    raise TypeError(f"Cannot apply NOT to non-boolean: {operand}")
                return not operand

            left_val = self._eval(left) if left else None
            right_val = self._eval(right)

            # Type checks based on operator
            if op.type in ('PLUS', 'MINUS', 'MUL', 'DIV'):
                if not self._are_compatible(left_val, right_val):
                    raise TypeError(f"Unsupported operand types: {type(left_val)} and {type(right_val)}")
            elif op.type in ('AND', 'OR'):
                if not (type(left_val) is bool and type(right_val) is bool):
                    raise TypeError(f"Logical operators require booleans, got {type(left_val)} and {type(right_val)}")
            elif op.type in ('EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE'):
                if not self._are_compatible(left_val, right_val, allow_number_bool=True):
                    raise TypeError(f"Cannot compare {type(left_val)} and {type(right_val)}")

            # Perform the operation
            if op.type == 'PLUS':
                return left_val + right_val
            elif op.type == 'MINUS':
                return left_val - right_val
            elif op.type == 'MUL':
                return left_val * right_val
            elif op.type == 'DIV':
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