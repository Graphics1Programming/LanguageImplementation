class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = None
        self.advance()

    def advance(self):
        self.current_token = self.scanner.get_next_token()

    def peek_next_token(self):
        # Peek next token without advancing the current token
        return self.scanner.peek_next_token()

    def parse(self):
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return ('BLOCK', statements)

    def statement(self):
        # Handle statements: make (DECL), del, print, if, while, assignment, or expression statement
        if self.current_token.type == 'MAKE':  # Variable assignment with 'make'
            return self.make_statement()
        elif self.current_token.type == 'DEL':  # Variable deletion with 'del'
            return self.del_statement()
        elif self.current_token.type == 'PRINT':
            return self.print_statement()
        elif self.current_token.type == 'IF':
            return self.if_statements()
        elif self.current_token.type == 'WHILE':
            return self.while_statement()
        elif self.current_token.type == 'VARIABLE':
            # Lookahead for assignment without 'make'
            next_token = self.peek_next_token()
            if next_token.type == 'ASSIGN':
                # Parse assignment like: x = expr
                var_token = self.current_token
                self.advance()  # consume variable
                self.advance()  # consume '='
                expr = self.boolean_expression()
                return ('ASSIGN', var_token, expr)
            else:
                # Not assignment, parse as expression statement
                return self.boolean_expression()
        else:
            # Expression statement
            return self.boolean_expression()

    def make_statement(self):
        self.advance()  # skip 'make'
        if self.current_token.type != 'VARIABLE':
            raise ValueError("Expected variable name after 'make'")
        var_token = self.current_token
        self.advance()
        if self.current_token.type != 'ASSIGN':
            raise ValueError("Expected '=' after variable in make statement")
        self.advance()  # skip '='
        expr = self.boolean_expression()
        return ('ASSIGN', var_token, expr)

    def del_statement(self):
        self.advance()  # skip 'del'
        if self.current_token.type != 'VARIABLE':
            raise ValueError("Expected variable name after 'del'")
        var_token = self.current_token
        self.advance()
        return ('DEL', var_token)

    def print_statement(self):
        self.advance()  # skip 'print'
        expr = self.boolean_expression()
        return ('PRINT', expr)

    def if_statements(self):
        conditions = []
        actions = []

        self.advance()  # skip 'if'
        cond = self.boolean_expression()
        if self.current_token.type != 'DO':
            raise ValueError("Expected 'do' after if condition")
        self.advance()  # skip 'do'
        action = self.statement()
        conditions.append(cond)
        actions.append(action)

        while self.current_token.type == 'ELIF':
            self.advance()  # skip 'elif'
            cond = self.boolean_expression()
            if self.current_token.type != 'DO':
                raise ValueError("Expected 'do' after elif condition")
            self.advance()  # skip 'do'
            action = self.statement()
            conditions.append(cond)
            actions.append(action)

        else_action = None
        if self.current_token.type == 'ELSE':
            self.advance()  # skip 'else'
            if self.current_token.type != 'DO':
                raise ValueError("Expected 'do' after else")
            self.advance()  # skip 'do'
            else_action = self.statement()

        return ('IF', conditions, actions, else_action)

    def while_statement(self):
        self.advance()  # skip 'while'
        condition = self.boolean_expression()
        if self.current_token.type != 'DO':
            raise ValueError("Expected 'do' after while condition")
        self.advance()  # skip 'do'
        action = self.statement()
        return ('WHILE', condition, action)

    # Expression parsing follows precedence and associativity
    def boolean_expression(self):
        node = self.comp_expression()
        while self.current_token.type in ('AND', 'OR'):
            op = self.current_token
            self.advance()
            right = self.comp_expression()
            node = (op, node, right)
        return node

    def comp_expression(self):
        node = self.expression()
        comparison_ops = ('EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE', 'CMP')
        while self.current_token.type in comparison_ops:
            op = self.current_token
            self.advance()
            right = self.expression()
            node = (op, node, right)
        return node

    def expression(self):
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token
            self.advance()
            right = self.term()
            node = (op, node, right)
        return node

    def term(self):
        node = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token
            self.advance()
            right = self.factor()
            node = (op, node, right)
        return node

    def factor(self):
        token = self.current_token

        if token.type in ('NUMBER', 'FLOAT', 'BOOL', 'STRING'):
            self.advance()
            return token

        elif token.type == 'VARIABLE':
            self.advance()
            return token

        elif token.type == 'LPAREN':
            self.advance()
            node = self.boolean_expression()
            if self.current_token.type != 'RPAREN':
                raise ValueError("Expected ')'")
            self.advance()
            return node

        elif token.type in ('MINUS', 'NOT'):
            op = token
            self.advance()
            operand = self.factor()
            return (op, None, operand)

        else:
            raise ValueError(f"Unexpected token in factor: {token}")
