class Data:
    def __init__(self):
        self.variables = {}  # Acts as the symbol table

    def read(self, identifier):
        name = identifier.value if hasattr(identifier, 'value') else identifier
        if name in self.variables:
            return self.variables[name]
        raise ValueError(f"Variable '{name}' not defined.")

    def write(self, identifier, value):
        name = identifier.value if hasattr(identifier, 'value') else identifier
        self.variables[name] = value

    def exists(self, identifier):
        name = identifier.value if hasattr(identifier, 'value') else identifier
        return name in self.variables

    def all(self):
        return self.variables
