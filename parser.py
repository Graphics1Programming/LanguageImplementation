from tokens import Token
class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = None
        self.advance()

    def advance(self):
        """Advance to the next token."""
        self.current_token = self.scanner.get_next_token()

    def parse(self):
        """Parse the entire input."""
        return self.expr()

    def expr(self):
        """Handle the main expression parsing: addition, subtraction, and boolean logic."""
        result = self.term()
        while self.current_token.type in ('PLUS', 'MINUS', 'OR'):
            token = self.current_token
            self.advance()
            right = self.term()
            result = (token, result, right)
        return result

    def term(self):
        """Handle multiplication, division, and comparisons."""
        result = self.factor()
        while self.current_token.type in ('MUL', 'DIV', 'AND'):
            token = self.current_token
            self.advance()
            right = self.factor()
            result = (token, result, right)
        return result

    def factor(self):
        """Handle unary negation, parentheses, and literal values."""
        token = self.current_token

        if token.type == 'MINUS':  # Unary negation
            self.advance()
            return ('NEGATE', self.factor())

        elif token.type == 'NUMBER' or token.type == 'FLOAT':
            self.advance()
            return token

        elif token.type == 'BOOL':
            self.advance()
            return token

        elif token.type == 'STRING':
            self.advance()
            return token

        elif token.type == 'LPAREN':
            self.advance()
            result = self.expr()
            if self.current_token.type != 'RPAREN':
                raise ValueError("Expected ')'")
            self.advance()
            return result

        raise ValueError(f"Unexpected token: {token}")
