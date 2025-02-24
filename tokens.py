class Token:
    TYPE_DISPLAY = {  # Fixed syntax: removed "class token"
        'LPAREN': '(',
        'RPAREN': ')',
        'NUMBER': 'NUMBER',
        'STRING': 'STRING',
        'PLUS': 'PLUS',
        'MINUS': 'MINUS',
        'MUL': 'MUL',
        'DIV': 'DIV',
        'BOOL': 'BOOL',
        'AND': 'AND',
        'OR': 'OR',
        'NOT': 'NOT',
        'EQ': 'EQUAL_TO',
        'NEQ': 'NOT_EQUAL',
        'LT': 'LESS_THAN',
        'GT': 'GREATER_THAN',
        'LTE': 'LESS_EQUAL',
        'GTE': 'GREATER_EQUAL',
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
            if self.type == 'STRING':
                return f'STRING("{self.value}")'
            return f"{display_type}({self.value})"
        return display_type