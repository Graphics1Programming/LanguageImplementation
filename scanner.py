from tokens import Token

class Scanner:
    """
    Scanner class for lexical analysis. Converts source text into tokens.
    Supports keywords, numbers, identifiers, strings, and various operators.
    """

    # Mapping of keywords to token types and their associated values
    keywords = {
        'true':   ('BOOL', True),
        'false':  ('BOOL', False),
        'and':    ('AND', 'and'),
        'or':     ('OR', 'or'),
        'not':    ('NOT', 'not'),
        'print':  ('PRINT', 'print'),
        'make':   ('MAKE', 'make'),
        'if':     ('IF', 'if'),
        'elif':   ('ELIF', 'elif'),
        'else':   ('ELSE', 'else'),
        'while':  ('WHILE', 'while'),
        'break':  ('BREAK', 'break'),
        'del':    ('DEL', 'del'),
        'input':  ('INPUT', 'input'),
        'int':    ('INT', 'int'),
    }

    def __init__(self, text):
        """
        Initialise the scanner with input text.
        Set the starting position and current character.
        """
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None
        self._peeked_token = None  # Cache for peeked token (lookahead)

    def advance(self):
        """Move the position one character forward."""
        self.position += 1
        self.current_char = self.text[self.position] if self.position < len(self.text) else None

    def skip_whitespace(self):
        """Skip whitespace characters (space, tab, newline, carriage return)."""
        while self.current_char is not None and self.current_char in ' \t\n\r':
            self.advance()

    def number(self):
        """
        Parse a number token (int or float).
        Returns a Token of type NUMBER or FLOAT.
        """
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
        """
        Parse an identifier or keyword.
        Returns a VARIABLE token or a specific keyword token.
        """
        value = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            value += self.current_char
            self.advance()

        lower = value.lower()
        if lower in self.keywords:
            token_type, token_value = self.keywords[lower]
            return Token(token_type, token_value)
        return Token('VARIABLE', value)

    def string(self):
        """
        Parse a string literal enclosed in double quotes.
        Handles escape sequences and returns STRING token.
        """
        self.advance()  # Skip opening quote
        result = ''
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char is None:
                    raise ValueError("Unclosed string literal with escape")
                escape_map = {'n': '\n', 't': '\t', '"': '"', '\\': '\\'}
                result += escape_map.get(self.current_char, '\\' + self.current_char)
            else:
                result += self.current_char
            self.advance()

        if self.current_char != '"':
            raise ValueError("Unclosed string literal")
        self.advance()  # Skip closing quote
        return Token('STRING', result)

    def operator(self):
        """
        Parse and return an operator token.
        Supports multi-character and single-character operators.
        """
        ops = [
            ('!=', 'NEQ'), ('==', 'EQ'), ('<=', 'LTE'), ('>=', 'GTE'), ('?=', 'QMARK_EQ'),
            ('!', 'NOT'), ('+', 'PLUS'), ('-', 'MINUS'), ('*', 'MUL'), ('/', 'DIV'),
            ('%', 'MOD'), ('<', 'LT'), ('>', 'GT'), ('=', 'ASSIGN'),
            ('(', 'LPAREN'), (')', 'RPAREN'), ('{', 'LBRACE'), ('}', 'RBRACE')
        ]

        for symbol, token_type in ops:
            end = self.position + len(symbol)
            if self.text[self.position:end] == symbol:
                for _ in range(len(symbol)):
                    self.advance()
                return Token(token_type, symbol)

        raise ValueError(f"Unknown operator or character: '{self.current_char}' at position {self.position}")

    def get_next_token(self):
        """
        Retrieve the next token from input.
        Handles whitespace, comments, literals, identifiers, and operators.
        Returns EOF token at end of input.
        """
        if self._peeked_token:
            token = self._peeked_token
            self._peeked_token = None
            return token

        while self.current_char is not None:
            if self.current_char in ' \t\n\r':
                self.skip_whitespace()
                continue

            if self.current_char == '#':
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                if self.current_char == '\n':
                    self.advance()
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
        """
        Peek at the next token without consuming it.
        Useful for lookahead during parsing.
        """
        if not self._peeked_token:
            self._peeked_token = self.get_next_token()
        return self._peeked_token
