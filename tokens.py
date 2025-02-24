class Token:
    TYPE_DISPLAY = {
        'LPAREN': '(',
        'RPAREN': ')',
        'NUMBER': 'NUMBER',
        'PLUS': '+',
        'MINUS': '-',
        'MUL': '*',
        'DIV': '/',
        'BOOL': 'BOOL',
        'AND': 'AND',
        'OR': 'OR',
        'NOT': '!',
        'EQ': '==',
        'NEQ': '!=',
        'LT': '<',
        'GT': '>',
        'LTE': '<=',
        'GTE': '>=',
        'EOF': 'EOF'
    }

    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

    def __str__(self):
        display_type = self.TYPE_DISPLAY.get(self.type, self.type)
        if self.value is not None:
            return f"{display_type}({self.value})"
        return display_type