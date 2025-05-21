class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = None
        self.advance()

    def advance(self):
        self.current_token = self.scanner.get_next_token()

    def parse(self):
        """Parses a sequence of statements (including assignments and prints)."""
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return 'BLOCK', statements

    def statement(self):
        """Parse a print statement, assignment, or expression."""
        if self.current_token.type == 'IDENTIFIER':
            var_token = self.current_token
            self.advance()
            if self.current_token.type == 'EQ':  # '=' operator
                self.advance()
                expr = self.logical_or()
                return 'ASSIGN', var_token.value, expr
            else:
                raise ValueError("Expected '=' after identifier")

        elif self.current_token.type == 'PRINT':
            return self.print_statement()

        else:
            return self.logical_or()

    def print_statement(self):
        """Parse a print statement: print <expression>"""
        self.advance()  # skip 'PRINT'
        expr = self.logical_or()
        return 'PRINT', expr

    def logical_or(self):
        node = self.logical_and()
        while self.current_token.type == 'OR':
            op = self.current_token.type
            self.advance()
            right = self.logical_and()
            node = op, node, right
        return node

    def logical_and(self):
        node = self.comparison()
        while self.current_token.type == 'AND':
            op = self.current_token.type
            self.advance()
            right = self.comparison()
            node = op, node, right
        return node

    def comparison(self):
        node = self.term()
        while self.current_token.type in ('EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE'):
            op = self.current_token.type
            self.advance()
            right = self.term()
            node = op, node, right
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token.type
            self.advance()
            right = self.factor()
            node = op, node, right
        return node

    def factor(self):
        node = self.unary()
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token.type
            self.advance()
            right = self.unary()
            node = op, node, right
        return node

    def unary(self):
        if self.current_token.type in ('MINUS', 'NOT'):
            op = self.current_token.type
            self.advance()
            operand = self.unary()
            return op, None, operand
        return self.primary()

    def primary(self):
        token = self.current_token

        if token.type in ('NUMBER', 'FLOAT', 'BOOL', 'STRING', 'IDENTIFIER'):
            self.advance()
            return token

        if token.type == 'LPAREN':
            self.advance()
            node = self.logical_or()
            if self.current_token.type != 'RPAREN':
                raise ValueError("Expected ')'")
            self.advance()
            return node

        raise ValueError(f"Unexpected token: {token}")
