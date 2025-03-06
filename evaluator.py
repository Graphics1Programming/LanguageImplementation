from tokens import Token

class Evaluator:
    def __init__(self, ast):
        self.ast = ast

    def evaluate(self):
        return self._eval(self.ast)

    def _eval(self, node):
        if isinstance(node, Token):
            if node.type == 'NUMBER':
                return node.value
            elif node.type == 'FLOAT':
                return node.value
            elif node.type == 'BOOL':
                return node.value
            elif node.type == 'STRING':
                return node.value

        if isinstance(node, tuple):
            operator, left, right = node

            if operator == 'NEGATE':
                return not self._eval(left)

            if operator.type == 'PLUS':
                return self._eval(left) + self._eval(right)
            elif operator.type == 'MINUS':
                return self._eval(left) - self._eval(right)
            elif operator.type == 'MUL':
                return self._eval(left) * self._eval(right)
            elif operator.type == 'DIV':
                return self._eval(left) / self._eval(right)

            elif operator.type == 'EQ':
                return self._eval(left) == self._eval(right)
            elif operator.type == 'NEQ':
                return self._eval(left) != self._eval(right)
            elif operator.type == 'LT':
                return self._eval(left) < self._eval(right)
            elif operator.type == 'GT':
                return self._eval(left) > self._eval(right)
            elif operator.type == 'LTE':
                return self._eval(left) <= self._eval(right)
            elif operator.type == 'GTE':
                return self._eval(left) >= self._eval(right)

            elif operator.type == 'AND':
                return self._eval(left) and self._eval(right)
            elif operator.type == 'OR':
                return self._eval(left) or self._eval(right)

            elif operator.type == 'NOT':
                return not self._eval(left)
