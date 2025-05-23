class Parser:
    def __init__(self, scanner):
        # Initialise the parser with a scanner instance
        self.scanner = scanner
        self.current_token = None
        self.advance()  # Load the first token

    def advance(self):
        # Get the next token from the scanner and update current_token
        self.current_token = self.scanner.get_next_token()

    def peek_next_token(self):
        # Peek at the next token without consuming it (without advancing)
        return self.scanner.peek_next_token()

    def parse(self):
        # Parse the entire input into a block of statements until EOF is reached
        statements = []
        while self.current_token.type != 'EOF':
            stmt = self.statement()
            statements.append(stmt)
        return ('BLOCK', statements)

    def statement(self):
        # Parse a statement, which could be one of several types:
        # variable declaration (make), deletion (del), printing, conditionals (if),
        # loops (while), assignment, or expression statements.
        if self.current_token.type == 'MAKE':  # 'make' keyword for declaration
            return self.make_statement()
        elif self.current_token.type == 'DEL':  # 'del' keyword for deletion
            return self.del_statement()
        elif self.current_token.type == 'PRINT':  # 'print' statement
            return self.print_statement()
        elif self.current_token.type == 'IF':  # if conditional block
            return self.if_statements()
        elif self.current_token.type == 'WHILE':  # while loop
            return self.while_statement()
        elif self.current_token.type == 'VARIABLE':
            # Check if it's an assignment (e.g., x = expr) without 'make'
            next_token = self.peek_next_token()
            if next_token.type == 'ASSIGN':
                var_token = self.current_token
                self.advance()  # consume variable
                self.advance()  # consume '='
                expr = self.boolean_expression()
                return ('ASSIGN', var_token, expr)
            else:
                # Otherwise treat as an expression statement
                return self.boolean_expression()
        else:
            # Parse as an expression statement if none of the above
            return self.boolean_expression()

    def make_statement(self):
        # Parse a 'make' variable declaration statement:
        # make <variable> = <expression>
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
        # Parse a 'del' statement to delete a variable:
        # del <variable>
        self.advance()  # skip 'del'
        if self.current_token.type != 'VARIABLE':
            raise ValueError("Expected variable name after 'del'")
        var_token = self.current_token
        self.advance()
        return ('DEL', var_token)

    def print_statement(self):
        # Parse a print statement:
        # print <expression>
        self.advance()  # skip 'print'
        expr = self.boolean_expression()
        return ('PRINT', expr)

    def if_statements(self):
        # Parse an if-elif-else conditional block
        conditions = []
        actions = []

        self.advance()  # skip 'if'
        cond = self.boolean_expression()  # condition expression
        if self.current_token.type != 'DO':
            raise ValueError("Expected 'do' after if condition")
        self.advance()  # skip 'do'
        action = self.statement()  # statement to execute if condition true
        conditions.append(cond)
        actions.append(action)

        # Parse zero or more 'elif' blocks
        while self.current_token.type == 'ELIF':
            self.advance()  # skip 'elif'
            cond = self.boolean_expression()
            if self.current_token.type != 'DO':
                raise ValueError("Expected 'do' after elif condition")
            self.advance()  # skip 'do'
            action = self.statement()
            conditions.append(cond)
            actions.append(action)

        # Parse optional 'else' block
        else_action = None
        if self.current_token.type == 'ELSE':
            self.advance()  # skip 'else'
            if self.current_token.type != 'DO':
                raise ValueError("Expected 'do' after else")
            self.advance()  # skip 'do'
            else_action = self.statement()

        return ('IF', conditions, actions, else_action)

    def while_statement(self):
        # Parse a while loop:
        # while <condition> do <statement>
        self.advance()  # skip 'while'
        condition = self.boolean_expression()
        if self.current_token.type != 'DO':
            raise ValueError("Expected 'do' after while condition")
        self.advance()  # skip 'do'
        action = self.statement()
        return ('WHILE', condition, action)

    # Expression parsing methods follow operator precedence and associativity rules

    def boolean_expression(self):
        # Parse expressions with boolean operators (and, or)
        node = self.comp_expression()
        while self.current_token.type in ('AND', 'OR'):
            op = self.current_token
            self.advance()
            right = self.comp_expression()
            node = (op, node, right)  # binary operation tuple
        return node

    def comp_expression(self):
        # Parse comparison expressions: ==, !=, <, >, <=, >=
        node = self.expression()
        comparison_ops = ('EQ', 'NEQ', 'LT', 'GT', 'LTE', 'GTE', 'CMP')
        while self.current_token.type in comparison_ops:
            op = self.current_token
            self.advance()
            right = self.expression()
            node = (op, node, right)
        return node

    def expression(self):
        # Parse addition and subtraction expressions
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token
            self.advance()
            right = self.term()
            node = (op, node, right)
        return node

    def term(self):
        # Parse multiplication and division expressions
        node = self.factor()
        while self.current_token.type in ('MUL', 'DIV'):
            op = self.current_token
            self.advance()
            right = self.factor()
            node = (op, node, right)
        return node

    def factor(self):
        # Parse a factor, which can be:
        # - a literal (number, float, bool, string)
        # - a variable
        # - a parenthesized expression
        # - unary operations like negation (-) or logical not (not)
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
            # Unary operator handling
            op = token
            self.advance()
            operand = self.factor()
            return (op, None, operand)

        else:
            raise ValueError(f"Unexpected token in factor: {token}")
