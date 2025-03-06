class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = None
        self.advance()

    def advance(self):
        self.current_token = self.scanner.get_next_token()

    def parse(self):
        return self.logical_or()

    def logical_or(self):
        """Handles OR operations (lowest precedence)."""
        node = self.logical_and()
        while self.current_token.type == 'OR':
            op = self.current_token
            self.advance()
            node = (op, node, self.logical_and())
        return node

    def logical_and(self):
        """Handles AND operations."""
        node = self.comparison()
        while self.current_token.type == 'AND':
            op = self.current_token
            self.advance()
            node = (op, node, self.comparison())
        return node

    def comparison(self):
        """Handles comparisons (e.g., ==, <, >)."""
        node = self.term()
        comparison_ops = ('EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE')
        while self.current_token.type in comparison_ops:
            op = self.current_token
            self.advance()
            node = (op, node, self.term())
        return node

    def term(self):
        """Handles addition and subtraction."""
        node = self.factor()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token
            self.advance()
            node = (op, node, self.factor())
        return node

    def factor(self):
        """Handles multiplication and division."""
        node = self.unary()
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token
            self.advance()
            node = (op, node, self.unary())
        return node

    def unary(self):
        """Handles unary operators (e.g., -, NOT)."""
        if self.current_token.type in ('MINUS', 'NOT'):
            op = self.current_token
            self.advance()
            return op, None, self.unary()  # ✅ Fixed redundant parentheses
        return self.primary()

    def primary(self):
        """Handles literals and parentheses."""
        token = self.current_token

        # Handle literals (numbers, booleans, strings)
        if token.type in ('NUMBER', 'FLOAT', 'BOOL', 'STRING'):
            self.advance()
            return token

        # Handle parentheses
        if token.type == 'LPAREN':
            self.advance()
            node = self.logical_or()  # Parse the expression inside
            if self.current_token.type != 'RPAREN':
                raise ValueError("Expected ')'")
            self.advance()
            return node

        raise ValueError(f"Unexpected token: {token}")