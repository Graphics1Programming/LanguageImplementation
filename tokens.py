class Token:
    TYPE_DISPLAY = {
        'LPAREN': '(', 'RPAREN': ')', 'NUMBER': 'NUMBER', 'FLOAT': 'FLOAT',
        'STRING': 'STRING', 'PLUS': '+', 'MINUS': '-', 'MUL': '*', 'DIV': '/',
        'BOOL': 'BOOL', 'AND': 'AND', 'OR': 'OR', 'NOT': 'NOT', 'EQ': '==',
        'NEQ': '!=', 'LT': '<', 'GT': '>', 'LTE': '<=', 'GTE': '>=', 'EOF': 'EOF'
    }

    def __init__(self, token_type, value=None):
        if token_type not in self.TYPE_DISPLAY:
            raise ValueError(f"Invalid token type: {token_type}")
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

    def __str__(self):
        display_type = self.TYPE_DISPLAY.get(self.type, self.type)
        if self.value is not None:
            if self.type == 'STRING':
                return f'STRING("{self.value}")'
            return f"{display_type}({self.value})"
        return display_type