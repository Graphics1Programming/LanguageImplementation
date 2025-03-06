from tokens import Token

class Scanner:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def _read_number(self):
        result = ''
        has_decimal = False
        while self.current_char and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_decimal: break
                has_decimal = True
            result += self.current_char
            self.advance()
        # Return as float if there's a decimal point; otherwise, return as int
        if has_decimal:
            return Token('FLOAT', float(result))  # Returning FLOAT token
        else:
            return Token('NUMBER', int(result))  # Returning NUMBER token

    def _read_string(self):
        self.advance()  # Skip opening "
        result = ''
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        if not self.current_char:
            raise Exception("Unclosed string literal")
        self.advance()  # Skip closing "
        return result

    def _read_identifier(self):
        result = ''
        while self.current_char and self.current_char.isalpha():
            result += self.current_char
            self.advance()
        return result.lower()

    def get_next_token(self):
        while self.current_char:
            if self.current_char.isspace():
                self.advance()
                continue

            # Handle string literals first
            if self.current_char == '"':
                return Token('STRING', self._read_string())

            # Handle true/false/and/or
            if self.current_char.isalpha():
                ident = self._read_identifier()
                if ident == 'true': return Token('BOOL', True)
                if ident == 'false': return Token('BOOL', False)
                if ident == 'and': return Token('AND')
                if ident == 'or': return Token('OR')
                raise Exception(f"Unknown identifier: {ident}")

            # Handle numbers (both integer and floating-point)
            if self.current_char.isdigit() or self.current_char == '.':
                return self._read_number()  # Call the method for reading numbers

            # Handle comparisons and operators
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('EQ')
                raise Exception("Expected '=='")

            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('NEQ')
                return Token('NOT')

            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('LTE')
                return Token('LT')

            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token('GTE')
                return Token('GT')

            # Existing operators
            if self.current_char == '+':
                self.advance()
                return Token('PLUS')

            if self.current_char == '-':
                self.advance()
                return Token('MINUS')

            if self.current_char == '*':
                self.advance()
                return Token('MUL')

            if self.current_char == '/':
                self.advance()
                return Token('DIV')

            if self.current_char == '(':
                self.advance()
                return Token('LPAREN')

            if self.current_char == ')':
                self.advance()
                return Token('RPAREN')

            raise Exception(f"Invalid character: {self.current_char}")

        return Token('EOF')
