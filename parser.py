from tokens import Token

class ASTNode: pass

class NumberNode(ASTNode):
    def __init__(self, value): self.value = value

class BoolNode(ASTNode):
    def __init__(self, value): self.value = value

class StringNode(ASTNode):
    def __init__(self, value): self.value = value

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOpNode(ASTNode):
    def __init__(self, op, right):
        self.op = op
        self.right = right
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = scanner.get_next_token()

    def _expect(self, token_type):
        if self.current_token.type != token_type:
            raise Exception(f"Expected {token_type}, got {self.current_token.type}")
        self.current_token = self.scanner.get_next_token()

    def parse(self):
        return self.logical_or()

    # --- Corrected method order ---
    def factor(self):
        token = self.current_token
        if token.type == 'LPAREN':
            self._expect('LPAREN')
            node = self.parse()
            self._expect('RPAREN')
            return node
        elif token.type == 'NOT':
            self._expect('NOT')
            return UnaryOpNode(token, self.factor())
        elif token.type == 'MINUS':
            self._expect('MINUS')
            return UnaryOpNode(Token('NEGATE', '-'), self.factor())
        elif token.type == 'BOOL':
            self._expect('BOOL')
            return BoolNode(token.value)
        elif token.type == 'NUMBER':
            self._expect('NUMBER')
            return NumberNode(token.value)
        elif token.type == 'STRING':
            self._expect('STRING')
            return StringNode(token.value)
        else:
            raise Exception(f"Unexpected token: {token.type}")

    def term(self):
        node = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token
            self._expect(op.type)
            node = BinOpNode(node, op, self.factor())
        return node

    def arith_expr(self):
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token
            self._expect(op.type)
            node = BinOpNode(node, op, self.term())
        return node

    def comparison(self):
        node = self.arith_expr()
        while self.current_token.type in ('EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE'):
            op = self.current_token
            self._expect(op.type)
            node = BinOpNode(node, op, self.arith_expr())
        return node

    def logical_and(self):
        node = self.comparison()
        while self.current_token.type == 'AND':
            op = self.current_token
            self._expect('AND')
            node = BinOpNode(node, op, self.comparison())
        return node

    def logical_or(self):
        node = self.logical_and()
        while self.current_token.type == 'OR':
            op = self.current_token
            self._expect('OR')
            node = BinOpNode(node, op, self.logical_and())
        return node