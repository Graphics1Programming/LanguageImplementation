class VariableNotDefinedError(Exception):
    pass

class Data:
    def __init__(self):
        self.variables = {}  # Acts as the global symbol table

    def read(self, identifier):
        name = identifier.value if hasattr(identifier, 'value') else identifier
        if name in self.variables:
            return self.variables[name]
        raise VariableNotDefinedError(f"Variable '{name}' not defined.")

    def write(self, identifier, value):
        name = identifier.value if hasattr(identifier, 'value') else identifier
        self.variables[name] = value

    def exists(self, identifier):
        name = identifier.value if hasattr(identifier, 'value') else identifier
        return name in self.variables

    def delete(self, identifier):
        """
        Deletes the variable if it exists, otherwise raises error.
        Supports 'del' or nil-like behavior.
        """
        name = identifier.value if hasattr(identifier, 'value') else identifier
        if name in self.variables:
            del self.variables[name]
        else:
            raise VariableNotDefinedError(f"Variable '{name}' not defined, cannot delete.")

    def all(self):
        """
        Returns the dictionary of all global variables.
        """
        return self.variables
