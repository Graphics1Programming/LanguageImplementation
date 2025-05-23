# Custom exception raised when trying to access an undefined variable
class VariableNotDefinedError(Exception):
    pass

class Data:
    def __init__(self):
        # Dictionary to store variables and their associated values
        # Acts as the symbol table for variable storage
        self.variables = {}

    def read(self, identifier):
        """
        Retrieve the value of a variable by its identifier.
        'identifier' can be a token object with a 'value' attribute or a string.
        Raises VariableNotDefinedError if variable is not found.
        """
        name = identifier.value if hasattr(identifier, 'value') else identifier
        if name in self.variables:
            return self.variables[name]
        raise VariableNotDefinedError(f"Variable '{name}' not defined.")

    def write(self, identifier, value):
        """
        Assign a value to a variable.
        'identifier' can be a token or string representing the variable name.
        Stores/updates the variable in the symbol table.
        """
        name = identifier.value if hasattr(identifier, 'value') else identifier
        self.variables[name] = value

    def exists(self, identifier):
        """
        Check if a variable exists in the storage.
        Returns True if it exists, False otherwise.
        """
        name = identifier.value if hasattr(identifier, 'value') else identifier
        return name in self.variables

    def delete(self, identifier):
        """
        Deletes a variable from storage.
        Raises VariableNotDefinedError if variable does not exist.
        Supports behavior similar to 'del' statement in Python.
        """
        name = identifier.value if hasattr(identifier, 'value') else identifier
        if name in self.variables:
            del self.variables[name]
        else:
            raise VariableNotDefinedError(f"Variable '{name}' not defined, cannot delete.")

    def all(self):
        """
        Return the full dictionary of all variables currently stored.
        Useful for inspection or debugging.
        """
        return self.variables
