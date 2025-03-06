from tokens import Token

class Scanner:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None

    def advance(self):
        self.position += 1
        self.current_char = self.text[self.position] if self.position < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char in (' ', '\t', '\n'):
            self.advance()

    def number(self):
        result = ''
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += '.'
            self.advance()
            while self.current_char and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token('FLOAT', float(result))
        return Token('NUMBER', int(result))

    def identifier(self):
        value = ''
        while self.current_char and (self.current_char.isalpha() or self.current_char == '_'):
            value += self.current_char
            self.advance()
        value_lower = value.lower()
        if value_lower in ('true', 'false'):
            return Token('BOOL', value_lower == 'true')
        elif value_lower in ('and', 'or', 'not'):
            return Token(value_lower.upper(), value_lower)
        else:
            raise ValueError(f"Unknown identifier: {value}")

    def string(self):
        self.advance()  # Skip opening "
        result = ''
        while self.current_char and self.current_char != '"':
            result += self.current_char
            self.advance()
        if not self.current_char:
            raise ValueError("Unclosed string")
        self.advance()  # Skip closing "
        return Token('STRING', result)

    def operator(self):
        ops = [
            ('!=', 'NEQ'), ('!', 'NOT'),
            ('==', 'EQ'), ('<=', 'LTE'), ('>=', 'GTE'),
            ('+', 'PLUS'), ('-', 'MINUS'), ('*', 'MUL'), ('/', 'DIV'),
            ('<', 'LT'), ('>', 'GT'), ('(', 'LPAREN'), (')', 'RPAREN')
        ]
        for symbol, token_type in ops:
            end = self.position + len(symbol)
            if self.text[self.position:end] == symbol:
                for _ in range(len(symbol)):
                    self.advance()
                return Token(token_type, symbol)
        raise ValueError(f"Unknown operator: {self.current_char}")

    def get_next_token(self):
        self.skip_whitespace()
        if not self.current_char:
            return Token('EOF')

        if self.current_char.isdigit():
            return self.number()

        if self.current_char.isalpha() or self.current_char == '_':
            return self.identifier()

        if self.current_char == '"':
            return self.string()

        return self.operator()