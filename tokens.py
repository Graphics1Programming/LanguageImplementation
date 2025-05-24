class Token:
    # Mapping of token types to their display representations
    # This dictionary helps translate token type names into
    # human-readable forms, useful for debugging and output.
    TYPE_DISPLAY = {
        # Groupings - used for syntax grouping in expressions/statements
        'LPAREN': '(',          # Left parenthesis
        'RPAREN': ')',          # Right parenthesis
        'LBRACE': '{',          # Left braces
        'RBRACE': '}',          # Right braces
        'NUMBER': 'NUMBER',     # Integer numbers
        'FLOAT': 'FLOAT',       # Floating point numbers
        'STRING': 'STRING',     # String literals
        'BOOL': 'BOOL',         # Boolean values (True/False)
        'IDENTIFIER': 'IDENTIFIER',  # Names like variable/function identifiers
        'VARIABLE': 'variable',       # Variable names (alternative identifier type)

        # Operators - symbols for mathematical and logical operations
        'PLUS': '+',            # Addition operator
        'MINUS': '-',           # Subtraction operator
        'MUL': '*',             # Multiplication operator
        'DIV': '/',             # Division operator
        'EQ': '==',             # Equality comparison operator
        'NEQ': '!=',            # Not equal comparison operator
        'LT': '<',              # Less than comparison operator
        'GT': '>',              # Greater than comparison operator
        'LTE': '<=',            # Less than or equal to comparison operator
        'GTE': '>=',            # Greater than or equal to comparison operator
        'QMARK_EQ': '?=',       # Custom operator, possibly conditional assignment
        'MOD': '%',             # Modulus operator token

        # Logical operators for boolean logic
        'AND': 'AND',           # Logical AND
        'OR': 'OR',             # Logical OR
        'NOT': 'NOT',           # Logical NOT

        # Keywords and control flow commands for the language
        'PRINT': 'PRINT',       # Print statement keyword
        'MAKE': 'MAKE',
        'INPUT': 'INPUT',
        'INT': 'int',

        # Possibly variable declaration or assignment keyword
        'IF': 'IF',             # If statement keyword
        'ELIF': 'ELIF',         # Else-if statement keyword
        'ELSE': 'ELSE',         # Else statement keyword
        'WHILE': 'WHILE',       # While loop keyword
        'BREAK': 'BREAK',       # Break statement keyword

        # New keyword for deletion operations
        'DEL': 'DEL',           # Delete keyword

        # Special tokens
        'ASSIGN': '=',          # Assignment operator
        'EOF': 'EOF'            # End of file/input token
    }

    def __init__(self, token_type, value=None):
        """
        Initialize a Token instance.
        :param token_type: The type of the token (must be in TYPE_DISPLAY).
        :param value: The optional value associated with the token (e.g., number or string literal).
        Raises ValueError if token_type is invalid.
        """
        if token_type not in self.TYPE_DISPLAY:
            raise ValueError(f"Invalid token type: {token_type}")
        self.type = token_type
        self.value = value

    def __repr__(self):
        """
        Official string representation of the token.
        Useful for debugging and logging.
        Example: Token(NUMBER, 123)
        """
        return f"Token({self.type}, {repr(self.value)})"

    def __str__(self):
        """
        Informal string representation of the token.
        Displays the token in a readable format.
        For example:
          - STRING tokens show as STRING("value")
          - Other tokens show as their display name with value if present.
        """
        display_type = self.TYPE_DISPLAY.get(self.type, self.type)
        if self.value is not None:
            if self.type == 'STRING':
                return f'STRING("{self.value}")'
            return f"{display_type}({self.value})"
        return display_type
