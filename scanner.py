from tokens import Token

class Scanner:
    def __init__(self, text):
        self.text = text
        self.position = 0
        self.current_char = self.text[self.position] if len(self.text) > 0 else None

    def advance(self):
        """Move to the next character."""
        self.position += 1
        if self.position < len(self.text):
            self.current_char = self.text[self.position]
        else:
            self.current_char = None

    def skip_whitespace(self):
        """Skip any whitespace characters."""
        while self.current_char is not None and self.current_char in ' \t\n':
            self.advance()

    def number(self):
        """Handle integer or floating point numbers."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        if self.current_char == '.':
            result += '.'
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()
            return Token('FLOAT', float(result))
        return Token('NUMBER', int(result))

    def boolean(self):
        """Handle boolean literals."""
        value = ''
        while self.current_char is not None and self.current_char.isalpha():
            value += self.current_char
            self.advance()
        if value.lower() == "true":
            return Token('BOOL', True)
        elif value.lower() == "false":
            return Token('BOOL', False)
        raise ValueError(f"Invalid boolean value: {value}")

    def string(self):
        """Handle string literals."""
        result = ''
        self.advance()  # Skip the opening quote
        while self.current_char != '"' and self.current_char is not None:
            result += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return Token('STRING', result)

    def operator(self):
        """Handle operators like +, -, *, /, etc."""
        operators = ['+', '-', '*', '/', '==', '!=', '(', ')', '<', '>', '<=', '>=', 'and', 'or', 'not']
        for op in operators:
            if self.text[self.position:self.position + len(op)] == op:
                self.advance()
                return Token(op, op)
        raise ValueError(f"Invalid operator: {self.current_char}")

    def get_next_token(self):
        """Return the next token in the input."""
        self.skip_whitespace()

        if self.current_char is None:
            return Token('EOF')

        if self.current_char.isdigit():
            return self.number()

        if self.current_char.isalpha():
            return self.boolean()

        if self.current_char == '"':
            return self.string()

        if self.current_char in '+-*/()<>':
            return self.operator()

        raise ValueError(f"Unknown character: {self.current_char}")
