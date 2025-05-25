class Token:
    # Mapping of token types to their display representations.
    # This is used for debugging and displaying tokens in human-readable form.
    TYPE_DISPLAY = {
        # Groupings - delimiters for grouping expressions or blocks
        'LPAREN': '(',           # Left parenthesis
        'RPAREN': ')',           # Right parenthesis
        'LBRACE': '{',           # Left brace
        'RBRACE': '}',           # Right brace
        'LSQUARE': '[',          # Left square bracket
        'RSQUARE': ']',          # Right square bracket

        # Literal types
        'NUMBER': 'NUMBER',      # Integer literal
        'FLOAT': 'FLOAT',        # Floating-point literal
        'STRING': 'STRING',      # String literal
        'BOOL': 'BOOL',          # Boolean literal
        'IDENTIFIER': 'IDENTIFIER',  # Generic identifier (e.g., variable or function name)
        'VARIABLE': 'variable',      # Specific variable name (optional distinction)

        # Arithmetic operators
        'PLUS': '+',             # Addition
        'MINUS': '-',            # Subtraction
        'MUL': '*',              # Multiplication
        'DIV': '/',              # Division
        'MOD': '%',              # Modulus

        # Comparison operators
        'EQ': '==',              # Equal to
        'NEQ': '!=',             # Not equal to
        'LT': '<',               # Less than
        'GT': '>',               # Greater than
        'LTE': '<=',             # Less than or equal to
        'GTE': '>=',             # Greater than or equal to

        # Custom/extended operators
        'QMARK_EQ': '?=',        # Possibly a conditional assignment operator
        'COMMA': ',',
        'DOT': '.',
        'COLON': ':',

        # Logical operators
        'AND': 'AND',            # Logical AND
        'OR': 'OR',              # Logical OR
        'NOT': 'NOT',            # Logical NOT

        # Keywords / control flow
        'PRINT': 'PRINT',        # Output statement
        'MAKE': 'MAKE',          # Possibly for variable creation
        'INPUT': 'INPUT',        # User input
        'INT': 'int',            # Type keyword for integer conversion or declaration
        'IN': 'in',


        'IF': 'IF',              # Conditional: if
        'ELIF': 'ELIF',          # Else if
        'ELSE': 'ELSE',          # Else
        'WHILE': 'WHILE',        # While loop
        'BREAK': 'BREAK',        # Break from loop
        'CONTINUE': 'CONTINUE',   # Continue from loop
        'FOR': 'FOR',             # For loop

        # Deletion
        'DEL': 'DEL',            # Delete keyword

        # Special tokens
        'ASSIGN': '=',           # Assignment operator
        'EOF': 'EOF'             # End of input/file
    }

    def __init__(self, token_type, value=None):
        """
        Create a new token object.

        Parameters:
        - token_type (str): A key from TYPE_DISPLAY that identifies the token's type.
        - value (optional): The associated value (e.g., actual number, string, etc.)

        Raises:
        - ValueError: If token_type is not recognised.
        """
        if token_type not in self.TYPE_DISPLAY:
            raise ValueError(f"Invalid token type: {token_type}")
        self.type = token_type
        self.value = value

    def __repr__(self):
        """
        Return the official string representation of the token.
        Example: Token(NUMBER, 123)
        Useful for logging and debugging.
        """
        return f"Token({self.type}, {repr(self.value)})"

    def __str__(self):
        """
        Return a human-readable string representation of the token.
        Used in pretty printing or debugging output.

        Examples:
        - STRING("hello") for string tokens
        - +(2) for a PLUS token with value 2 (if applicable)
        """
        display_type = self.TYPE_DISPLAY.get(self.type, self.type)
        if self.value is not None:
            if self.type == 'STRING':
                return f'STRING("{self.value}")'
            return f"{display_type}({self.value})"
        return display_type
