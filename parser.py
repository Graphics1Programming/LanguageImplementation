class Parser:
    def __init__(self, scanner):
        self.scanner = scanner
        self.current_token = None
        self.advance()

    # Move to the next token
    def advance(self):
        self.current_token = self.scanner.get_next_token()

    # Peek the upcoming token without consuming it
    def peek_next_token(self):
        return self.scanner.peek_next_token()

    # ==== Core Parser Control ====
    def parse(self):
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.statement()
            if stmt is not None:
                statements.append(stmt)
            else:
                break  # End of block or invalid token
        return ('BLOCK', statements)

    # ==== Statement Dispatcher ====
    def statement(self):
        if self.current_token.type == 'RBRACE':
            return None  # End of block

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
        elif self.current_token.type == 'CONTINUE':
            self.advance()
            return ('CONTINUE',)
        elif self.current_token.type == 'VARIABLE':
            next_token = self.peek_next_token()
            if next_token.type == 'ASSIGN':
                var_token = self.current_token
                self.advance()  # VARIABLE
                self.advance()  # ASSIGN
                expr = self.boolean_expression()
                return ('ASSIGN', var_token, expr)
            else:
                return self.boolean_expression()
        elif self.current_token.type in ('ELSE', 'ELIF'):
            return None  # handled in if_statements()
        else:
            return self.boolean_expression()

    # ==== Specific Statement Parsers ====
    def make_statement(self):
        self.advance()  # consume 'MAKE'
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
        self.advance()  # consume 'DEL'
        if self.current_token.type != 'VARIABLE':
            raise ValueError("Expected variable name after 'del'")
        var_token = self.current_token
        self.advance()
        return ('DEL', var_token)

    def print_statement(self):
        self.advance()  # consume 'PRINT'
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
                break

        self.advance()  # consume '}'
        return statements[0] if len(statements) == 1 else ('BLOCK', statements)

    # ==== Conditional & Loop Handling ====
    def if_statements(self):
        conditions = []
        actions = []

        self.advance()  # consume 'IF'
        cond = self.boolean_expression()

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
            # Removed colon check and advance
            else_action = self.parse_block()

        return ('IF', conditions, actions, else_action)

    def while_statement(self):
        self.advance()  # consume 'WHILE'
        condition = self.boolean_expression()

        action = self.parse_block()
        return ('WHILE', condition, action)

    # ==== Boolean & Expression Parsing ====
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
            node = (op, node, right)
        return node

    # ==== Factors & Literals ====
    def factor(self):
        token = self.current_token


        if token.type in ('RBRACE', 'LBRACE', 'ELSE', 'ELIF', 'EOF'):
            raise StopIteration("End of expression reached due to block delimiter or control token")

        if token.type in ('NUMBER', 'FLOAT', 'BOOL', 'STRING'):
            self.advance()
            return token

        elif token.type in ('VARIABLE', 'INT'):
            if token.value == 'int':
                next_token = self.peek_next_token()
                if next_token.type == 'LPAREN':
                    self.advance()  # consume 'int'
                    self.advance()  # consume '('
                    expr = self.boolean_expression()
                    if self.current_token.type != 'RPAREN':
                        raise ValueError("Expected ')' after int() argument")
                    self.advance()  # consume ')'
                    return ('INT_CAST', expr)
                else:
                    self.advance()
                    node = token

                    # Handle list access variable[expr]
                    while self.current_token.type == 'LSQUARE':
                        self.advance()  # consume '['
                        index_expr = self.boolean_expression()
                        if self.current_token.type != 'RSQUARE':
                            raise ValueError("Expected ']' after list index")
                        self.advance()  # consume ']'
                        node = ('LIST_ACCESS', node, index_expr)

                    # --- Handle method calls obj.method(args) ---
                    while self.current_token.type == 'DOT':
                        self.advance()  # consume '.'

                        if self.current_token.type != 'VARIABLE':
                            raise ValueError("Expected method name after '.'")

                        method_name = self.current_token
                        self.advance()  # consume method name

                        if self.current_token.type != 'LPAREN':
                            raise ValueError("Expected '(' after method name")

                        self.advance()  # consume '('

                        args = []
                        if self.current_token.type != 'RPAREN':  # if method has args
                            args.append(self.boolean_expression())
                            while self.current_token.type == 'COMMA':
                                self.advance()  # consume ','
                                args.append(self.boolean_expression())

                        if self.current_token.type != 'RPAREN':
                            raise ValueError("Expected ')' after method arguments")

                        self.advance()  # consume ')'

                        node = ('METHOD_CALL', node, method_name, args)

                    return node

            else:
                self.advance()
                node = token

                # Handle list access variable[expr]
                while self.current_token.type == 'LSQUARE':
                    self.advance()  # consume '['
                    index_expr = self.boolean_expression()
                    if self.current_token.type != 'RSQUARE':
                        raise ValueError("Expected ']' after list index")
                    self.advance()  # consume ']'
                    node = ('LIST_ACCESS', node, index_expr)

                # --- Handle method calls obj.method(args) ---
                while self.current_token.type == 'DOT':
                    self.advance()  # consume '.'

                    if self.current_token.type != 'VARIABLE':
                        raise ValueError("Expected method name after '.'")

                    method_name = self.current_token
                    self.advance()  # consume method name

                    if self.current_token.type != 'LPAREN':
                        raise ValueError("Expected '(' after method name")

                    self.advance()  # consume '('

                    args = []
                    if self.current_token.type != 'RPAREN':  # if method has args
                        args.append(self.boolean_expression())
                        while self.current_token.type == 'COMMA':
                            self.advance()  # consume ','
                            args.append(self.boolean_expression())

                    if self.current_token.type != 'RPAREN':
                        raise ValueError("Expected ')' after method arguments")

                    self.advance()  # consume ')'

                    node = ('METHOD_CALL', node, method_name, args)

                return node

        elif token.type == 'LPAREN':
            self.advance()

            node = self.boolean_expression()

            if self.current_token.type != 'RPAREN':
                raise ValueError("Expected ')'")
            self.advance()
            return node

        elif token.type == 'LSQUARE':
            return self.parse_list_literal()

        elif token.type in ('MINUS', 'NOT'):
            op = token
            self.advance()
            operand = self.factor()
            return (op, None, operand)

        elif token.type == 'INPUT':
            return self.parse_input_expression()

        else:
            raise ValueError(f"Unexpected token in factor: {token}")

    # ==== Input Expression ====
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

    def parse_list_literal(self):
        self.advance()  # consume '['
        elements = []

        if self.current_token.type != 'RSQUARE':  # if not empty list
            elements.append(self.boolean_expression())
            while self.current_token.type == 'COMMA':
                self.advance()  # consume ','
                elements.append(self.boolean_expression())

        if self.current_token.type != 'RSQUARE':
            raise ValueError("Expected ']' to close list literal")
        self.advance()  # consume ']'

        return ('LIST_LITERAL', elements)
