class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = None
        self.advance()

    def advance(self):
        self.current_token = self.scanner.get_next_token()

    def peek_next_token(self):
        return self.scanner.peek_next_token()

    def parse(self):
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
            else:
                # No statement returned, maybe block end or control token
                break
        return ('BLOCK', statements)

    def statement(self):

        if self.current_token.type == 'RBRACE':
            # End of current block, return control to parse_block()
            return None
        if self.current_token.type == 'MAKE':
            return self.make_statement()
        elif self.current_token.type == 'DEL':
            return self.del_statement()
        elif self.current_token.type == 'PRINT':
            return self.print_statement()
        elif self.current_token.type == 'IF':
            return self.if_statements()
        elif self.current_token.type == 'WHILE':
            return self.while_statement()
        elif self.current_token.type == 'BREAK':
            self.advance()
            return ('BREAK',)
        elif self.current_token.type == 'VARIABLE':
            next_token = self.peek_next_token()
            if next_token.type == 'ASSIGN':
                var_token = self.current_token
                self.advance()
                self.advance()
                expr = self.boolean_expression()
                return ('ASSIGN', var_token, expr)
            else:
                return self.boolean_expression()
        elif self.current_token.type in ('ELSE', 'ELIF'):
            # Don't parse expression on else/elif, control should return to if_statements()
            return None
        else:
            return self.boolean_expression()

    def make_statement(self):
        self.advance()
        if self.current_token.type != 'VARIABLE':
            raise ValueError("Expected variable name after 'make'")
        var_token = self.current_token
        self.advance()
        if self.current_token.type != 'ASSIGN':
            raise ValueError("Expected '=' after variable in make statement")
        self.advance()
        expr = self.boolean_expression()
        return ('ASSIGN', var_token, expr)

    def del_statement(self):
        self.advance()
        if self.current_token.type != 'VARIABLE':
            raise ValueError("Expected variable name after 'del'")
        var_token = self.current_token
        self.advance()
        return ('DEL', var_token)

    def print_statement(self):
        self.advance()
        expr = self.boolean_expression()
        return ('PRINT', expr)

    def parse_block(self):
        if self.current_token.type != 'LBRACE':
            return self.statement()

        self.advance()  # consume '{'
        statements = []

        while self.current_token.type != 'RBRACE':
            if self.current_token.type == 'EOF':
                raise ValueError("Expected '}' before EOF")

            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
            else:
                # If statement() returns None, it means we hit a '}' or invalid token
                break

        self.advance()  # consume '}'

        if len(statements) == 1:
            return statements[0]
        else:
            return ('BLOCK', statements)

    def if_statements(self):
        conditions = []
        actions = []

        self.advance()  # consume 'if'
        cond = self.boolean_expression()

        # parse the block after if condition
        action = self.parse_block()

        conditions.append(cond)
        actions.append(action)

        while self.current_token.type == 'ELIF':
            self.advance()
            cond = self.boolean_expression()
            action = self.parse_block()
            conditions.append(cond)
            actions.append(action)

        else_action = None
        if self.current_token.type == 'ELSE':
            self.advance()
            else_action = self.parse_block()

        return ('IF', conditions, actions, else_action)

    def while_statement(self):
        self.advance()  # consume 'while'
        condition = self.boolean_expression()

        action = self.parse_block()

        return ('WHILE', condition, action)

    # Boolean expressions with AND/OR
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
        while self.current_token.type in ('MUL', 'DIV', 'MOD'):
            op = self.current_token
            self.advance()
            right = self.factor()
            node = (op, node, right)  # left and right can be tokens or tuples (nodes)
        return node

    def factor(self):
        token = self.current_token

        # Stop parsing factor on block delimiters or control tokens
        if token.type in ('RBRACE', 'LBRACE', 'ELSE', 'ELIF', 'EOF'):
            raise StopIteration("End of expression reached due to block delimiter or control token")

        if token.type in ('NUMBER', 'FLOAT', 'BOOL', 'STRING'):
            self.advance()
            return token

        # Handle both VARIABLE and INT token types for 'int' keyword
        elif token.type in ('VARIABLE', 'INT'):
            if token.value == 'int':
                next_token = self.peek_next_token()
                if next_token.type == 'LPAREN':
                    self.advance()  # consume 'int'
                    self.advance()  # consume '('
                    expr = self.boolean_expression()  # parse expression inside int()
                    if self.current_token.type != 'RPAREN':
                        raise ValueError("Expected ')' after int() argument")
                    self.advance()  # consume ')'
                    return ('INT_CAST', expr)
                else:
                    self.advance()
                    return token
            else:
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

        elif token.type == 'INPUT':
            return self.parse_input_expression()

        else:
            raise ValueError(f"Unexpected token in factor: {token}")

    def parse_input_expression(self):
        self.advance()  # consume 'INPUT'
        if self.current_token.type != 'LPAREN':
            raise ValueError("Expected '(' after 'input'")
        self.advance()  # consume '('

        prompt_expr = self.boolean_expression()

        if self.current_token.type != 'RPAREN':
            raise ValueError("Expected ')' after input prompt expression")
        self.advance()  # consume ')'

        return ('INPUT', prompt_expr)
