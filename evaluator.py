class Evaluator:
    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == 'PLUS':
            return left + right
        elif node.op.type == 'MINUS':
            return left - right
        elif node.op.type == 'MUL':
            return left * right
        elif node.op.type == 'DIV':
            return left / right

    def visit_UnaryOp(self, node):
        return -self.visit(node.expr)

    def visit_Num(self, node):
        return node.value