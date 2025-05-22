from tokens import Token

class Scanner:
    keywords = {
        'true': ('BOOL', True),
        'false': ('BOOL', False),
        'and': ('AND', 'and'),
        'or': ('OR', 'or'),
        'not': ('NOT', 'not'),
        'print': ('PRINT', 'print'),
        'make': ('MAKE', 'make'),
        'if': ('IF', 'if'),
        'elif': ('ELIF', 'elif'),
        'else': ('ELSE', 'else'),
        'do': ('DO', 'do'),
        'while': ('WHILE', 'while'),
    }

    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None
        self._peeked_token = None  # cache for peeked token

    def advance(self):
        self.position += 1
        self.current_char = self.text[self.position] if self.position < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char in (' ', '\t', '\n', '\r'):
            self.advance()

    def number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        # Check for float
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
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            value += self.current_char
            self.advance()
        value_lower = value.lower()
        if value_lower in self.keywords:
            token_type, token_val = self.keywords[value_lower]
            return Token(token_type, token_val)
        return Token('VARIABLE', value)

    def string(self):
        self.advance()  # Skip opening "
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        if self.current_char != '"':
            raise ValueError("Unclosed string literal")
        self.advance()  # Skip closing "
        return Token('STRING', result)

    def operator(self):
        # Order is important: longer symbols first to avoid premature matches
        ops = [
            ('!=', 'NEQ'), ('==', 'EQ'), ('<=', 'LTE'), ('>=', 'GTE'), ('?=', 'QMARK_EQ'),
            ('!', 'NOT'), ('+', 'PLUS'), ('-', 'MINUS'), ('*', 'MUL'), ('/', 'DIV'),
            ('<', 'LT'), ('>', 'GT'), ('=', 'ASSIGN'), ('(', 'LPAREN'), (')', 'RPAREN')
        ]
        for symbol, token_type in ops:
            end = self.position + len(symbol)
            if self.text[self.position:end] == symbol:
                for _ in range(len(symbol)):
                    self.advance()
                return Token(token_type, symbol)
        raise ValueError(f"Unknown operator or character: '{self.current_char}' at position {self.position}")

    def get_next_token(self):
        # If we have a peeked token, return it and clear the cache
        if self._peeked_token is not None:
            token = self._peeked_token
            self._peeked_token = None
            return token

        while self.current_char is not None:
            if self.current_char in (' ', '\t', '\n', '\r'):
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

    def peek_next_token(self):
        # If we already peeked, return cached token
        if self._peeked_token is not None:
            return self._peeked_token

        # Otherwise get the next token and cache it
        self._peeked_token = self.get_next_token()
        return self._peeked_token
