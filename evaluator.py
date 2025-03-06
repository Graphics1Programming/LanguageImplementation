from parser import NumberNode, BoolNode, StringNode, BinOpNode, UnaryOpNode

class Evaluator:
    @staticmethod
    def _is_numeric(a, b):
        """Check if both operands are either int or float"""
        return isinstance(a, (int, float)) and isinstance(b, (int, float))

    def _validate_operands(self, left, right, allowed_types, operator):
        """Ensure operands match required types or are compatible"""
        if (int in allowed_types or float in allowed_types) and self._is_numeric(left, right):
            return  # Allow mixed int and float operations
        if not (isinstance(left, allowed_types) and isinstance(right, allowed_types)):
            received = f"{type(left).__name__} and {type(right).__name__}"
            raise Exception(
                f"{operator} requires {allowed_types[0].__name__} operands, got {received}"
            )

    def evaluate(self, node):
        if isinstance(node, NumberNode):
            return node.value
        if isinstance(node, BoolNode):
            return node.value
        if isinstance(node, StringNode):
            return node.value

        if isinstance(node, UnaryOpNode):
            right = self.evaluate(node.right)
            if node.op.type == 'NOT':
                if not isinstance(right, bool):
                    raise Exception(f"! operator requires boolean, got {type(right).__name__}")
                return not right
            if node.op.type == 'NEGATE':
                if not isinstance(right, (int, float)):
                    raise Exception(f"- operator requires number, got {type(right).__name__}")
                return -right

        if isinstance(node, BinOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            op_type = node.op.type

            # Handle arithmetic operations
            if op_type in ('PLUS', 'MINUS', 'MUL', 'DIV'):
                if op_type == 'PLUS' and isinstance(left, str):
                    self._validate_operands(left, right, (str,), '+')
                    return left + right
                else:
                    self._validate_operands(left, right, (int, float), op_type)
                    if op_type == 'DIV' and right == 0:
                        raise Exception("Division by zero error")
                    return {
                        'PLUS': lambda a, b: a + b,
                        'MINUS': lambda a, b: a - b,
                        'MUL': lambda a, b: a * b,
                        'DIV': lambda a, b: a / b
                    }[op_type](left, right)

            # Handle comparisons
            if op_type in ('EQ', 'NEQ'):
                return {
                    'EQ': left == right,
                    'NEQ': left != right
                }[op_type]

            if op_type in ('LT', 'GT', 'LTE', 'GTE'):
                self._validate_operands(left, right, (int, float, str), op_type)
                return {
                    'LT': left < right,
                    'GT': left > right,
                    'LTE': left <= right,
                    'GTE': left >= right
                }[op_type]

            # Handle logical operators
            if op_type in ('AND', 'OR'):
                self._validate_operands(left, right, (bool,), op_type)
                return left and right if op_type == 'AND' else left or right

        raise Exception(f"Unhandled node type: {type(node).__name__}")
