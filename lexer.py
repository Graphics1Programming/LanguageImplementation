class Token:
    TYPE_NAMES = {
        'LPAREN': 'Left Parenthesis',
        'RPAREN': 'Right Parenthesis',
        'NUMBER': 'Number',
        'PLUS': 'Plus',
        'MINUS': 'Minus',
        'MUL': 'Multiply',
        'DIV': 'Divide',
        'EOF': 'End of File'
    }

    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

    def __str__(self):
        # Human-readable format for visualization
        friendly_type = self.TYPE_NAMES.get(self.type, self.type)
        if self.value is not None:
            return f"{friendly_type}({self.value})"
        return f"{friendly_type}"


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def number(self):
        result = ''
        has_decimal = False
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_decimal:
                    break
                has_decimal = True
            result += self.current_char
            self.advance()
        return float(result) if has_decimal or '.' in result else int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit() or self.current_char == '.':
                return Token('NUMBER', self.number())

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