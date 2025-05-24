from tokens import Token

class Scanner:
    # Mapping of keywords to their token types and corresponding values
    # This helps recognize reserved words in the source text.
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
        'while': ('WHILE', 'while'),
        'break': ('BREAK', 'break'),
        'del': ('DEL', 'del'),
        'input': ('INPUT', 'input'),
        'int': ('INT', 'int'),
    }

    def __init__(self, text):
        """
        Initialise the scanner with the input text.
        Set the starting position and current character.
        """
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if self.text else None
        self._peeked_token = None  # Cache for peeked token, supports lookahead

    def advance(self):
        """
        Move the position pointer one character forward.
        Update current_char or set to None if at end of text.
        """
        self.position += 1
        self.current_char = self.text[self.position] if self.position < len(self.text) else None

    def skip_whitespace(self):
        """
        Skip all whitespace characters (space, tab, newline, carriage return).
        Advances until a non-whitespace char or end of input is reached.
        """
        while self.current_char is not None and self.current_char in (' ', '\t', '\n', '\r'):
            self.advance()

    def number(self):
        """
        Parse a numeric token (integer or float).
        Accumulates digits; if a dot is found, parses fractional part.
        Returns Token of type NUMBER or FLOAT.
        Raises ValueError if float format is invalid.
        """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        # Check if next char is a dot for floating point number
        if self.current_char == '.':
            result += '.'
            self.advance()
            # After dot, must have at least one digit
            if self.current_char is None or not self.current_char.isdigit():
                raise ValueError(f"Invalid float literal at position {self.position}")
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token('FLOAT', float(result))

        # Otherwise, return integer token
        return Token('NUMBER', int(result))

    def identifier(self):
        """
        Parse an identifier or keyword.
        Identifiers can contain letters, digits, and underscores.
        Checks if the parsed value is a keyword; returns corresponding token.
        Otherwise, returns a VARIABLE token.
        """
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
        """
        Parse a string literal enclosed in double quotes.
        Handles escape sequences like \n, \t, \", and \\.
        Raises ValueError if string is not properly closed.
        Returns a STRING token with the interpreted content.
        """
        self.advance()  # Skip opening quote "
        result = ''
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char is None:
                    raise ValueError("Unclosed string literal with escape")
                if self.current_char == 'n':
                    result += '\n'
                elif self.current_char == 't':
                    result += '\t'
                elif self.current_char == '"':
                    result += '"'
                elif self.current_char == '\\':
                    result += '\\'
                else:
                    # For unsupported escape sequences, include them literally
                    result += '\\' + self.current_char
            else:
                result += self.current_char
            self.advance()
        if self.current_char != '"':
            raise ValueError("Unclosed string literal")
        self.advance()  # Skip closing quote "
        return Token('STRING', result)

    def operator(self):
        ops = [
            ('!=', 'NEQ'), ('==', 'EQ'), ('<=', 'LTE'), ('>=', 'GTE'), ('?=', 'QMARK_EQ'),
            ('!', 'NOT'), ('+', 'PLUS'), ('-', 'MINUS'), ('*', 'MUL'), ('/', 'DIV'), ('%', 'MOD'),
            ('<', 'LT'), ('>', 'GT'), ('=', 'ASSIGN'), ('(', 'LPAREN'), (')', 'RPAREN'), ('{', 'LBRACE'),
            ('}', 'RBRACE')
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
        Retrieve the next token from the input text.
        Handles skipping whitespace, comments, detecting numbers, identifiers,
        strings, operators, and returns EOF token at the end.
        Supports returning a cached peeked token if available.
        """
        # Return peeked token if exists, clearing the cache
        if self._peeked_token is not None:
            token = self._peeked_token
            self._peeked_token = None
            return token

        # Loop until a valid token is found or end of input reached
        while self.current_char is not None:
            # Skip whitespace
            if self.current_char in (' ', '\t', '\n', '\r'):
                self.skip_whitespace()
                continue

            # Skip comments starting with #
            if self.current_char == '#':
                # Skip everything until end of line or end of input
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                # After skipping comment line, skip the newline char too
                if self.current_char == '\n':
                    self.advance()
                continue  # Continue to next token

            # Number token (int or float)
            if self.current_char.isdigit():
                return self.number()

            # Identifier or keyword
            if self.current_char.isalpha() or self.current_char == '_':
                return self.identifier()

            # String literal
            if self.current_char == '"':
                return self.string()

            # Operators and punctuation
            return self.operator()

        # End of input reached; return EOF token
        return Token('EOF', None)

    def peek_next_token(self):
        """
        Look ahead to the next token without consuming it.
        Caches the token to be returned by next get_next_token call.
        """
        # Return cached token if already peeked
        if self._peeked_token is not None:
            return self._peeked_token

        # Get next token and cache it
        self._peeked_token = self.get_next_token()
        return self._peeked_token
