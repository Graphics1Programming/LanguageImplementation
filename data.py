# Custom exception raised when trying to access an undefined variable
class VariableNotDefinedError(Exception):
    pass

class Data:
    def __init__(self):
        # Internal storage for variables (symbol table)
        self.variables = {}

    def read(self, identifier):
        """
        Retrieve the value of a variable.

        Parameters:
        - identifier: A string or a token object with a 'value' attribute representing the variable name.

        Returns:
        - The value associated with the variable.

        Raises:
        - VariableNotDefinedError: If the variable does not exist.
        """
        name = identifier.value if hasattr(identifier, 'value') else identifier
        if name in self.variables:
            return self.variables[name]
        raise VariableNotDefinedError(f"Variable '{name}' not defined.")

    def write(self, identifier, value):
        """
        Assign a value to a variable.

        Parameters:
        - identifier: A string or token object representing the variable name.
        - value: The value to assign to the variable.

        Action:
        - Adds or updates the variable in the symbol table.
        """
        name = identifier.value if hasattr(identifier, 'value') else identifier
        self.variables[name] = value

    def exists(self, identifier):
        """
        Check if a variable exists.

        Parameters:
        - identifier: A string or token object representing the variable name.

        Returns:
        - True if the variable exists, False otherwise.
        """
        name = identifier.value if hasattr(identifier, 'value') else identifier
        return name in self.variables

    def delete(self, identifier):
        """
        Delete a variable from the symbol table.

        Parameters:
        - identifier: A string or token object representing the variable name.

        Raises:
        - VariableNotDefinedError: If the variable does not exist.
        """
        name = identifier.value if hasattr(identifier, 'value') else identifier
        if name in self.variables:
            del self.variables[name]
        else:
            raise VariableNotDefinedError(f"Variable '{name}' not defined, cannot delete.")

    def all(self):
        """
        Get the entire variable storage.

        Returns:
        - A dictionary of all stored variables and their values.
        Useful for debugging or inspection.
        """
        return self.variables
