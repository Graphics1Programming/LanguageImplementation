from parser import NumberNode, BoolNode, BinOpNode, UnaryOpNode

class Evaluator:
    def evaluate(self, node):
        if isinstance(node, NumberNode):
            return node.value
        if isinstance(node, BoolNode):
            return node.value
        if isinstance(node, UnaryOpNode):
            right = self.evaluate(node.right)
            if node.op.type == 'NOT':
                if not isinstance(right, bool):
                    raise Exception("! operator requires boolean")
                return not right
            if node.op.type == 'NEGATE':
                if not isinstance(right, (int, float)):
                    raise Exception("- operator requires number")
                return -right
        if isinstance(node, BinOpNode):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            # Type checking
            if node.op.type in ('EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE'):
                if type(left) != type(right):
                    raise Exception(f"Type mismatch: {type(left)} vs {type(right)}")
            # Operations
            if node.op.type == 'PLUS': return left + right
            if node.op.type == 'MINUS': return left - right
            if node.op.type == 'MUL': return left * right
            if node.op.type == 'DIV': return left / right
            if node.op.type == 'EQ': return left == right
            if node.op.type == 'NEQ': return left != right
            if node.op.type == 'LT': return left < right
            if node.op.type == 'GT': return left > right
            if node.op.type == 'LTE': return left <= right
            if node.op.type == 'GTE': return left >= right
            if node.op.type == 'AND': return left and right
            if node.op.type == 'OR': return left or right
        raise Exception(f"Unknown node type: {type(node)}")