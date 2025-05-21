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
        while self.current_char is not None and self.current_char in (' ', '\t', '\n'):
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += '.'
            self.advance()
            if self.current_char is None or not self.current_char.isdigit():
                raise ValueError(f"Invalid float literal at position {self.position}")
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token('FLOAT', float(result))
        return Token('NUMBER', int(result))

    def identifier(self):
        value = ''
        while self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
            value += self.current_char
            self.advance()
        value_lower = value.lower()
        if value_lower in ('true', 'false'):
            return Token('BOOL', value_lower == 'true')
        elif value_lower in ('and', 'or', 'not', 'print'):
            return Token(value_lower.upper(), value_lower)
        else:
            raise ValueError(f"Unknown identifier: {value}")

    def string(self):
        self.advance()  # Skip opening "
        result = ''
        while self.current_char is not None and self.current_char != '"':
            # Optional: Support escape sequences here if needed
            result += self.current_char
            self.advance()
        if self.current_char != '"':
            raise ValueError("Unclosed string literal")
        self.advance()  # Skip closing "
        return Token('STRING', result)

    def operator(self):
        ops = [
            ('!=', 'NEQ'), ('==', 'EQ'), ('<=', 'LTE'), ('>=', 'GTE'),
            ('!', 'NOT'),
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
        while self.current_char is not None:
            if self.current_char in (' ', '\t', '\n'):
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return self.number()

            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            if self.current_char == '"':
                return self.string()

            return self.operator()

        return Token('EOF', None)
