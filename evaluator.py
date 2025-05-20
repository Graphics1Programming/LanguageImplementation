from tokens import Token
from scanner import Scanner
from parser import Parser

class Evaluator:
    def evaluate(self, ast):
        return self._eval(ast)

    @staticmethod
    def _are_compatible(a, b, operator):
        """Check if two values are compatible for an operation based on the operator."""
        if operator == 'PLUS':
            # Allow addition if both are numbers or both are strings
            return (isinstance(a, (int, float)) and isinstance(b, (int, float))) or \
                   (isinstance(a, str) and isinstance(b, str))
        elif operator in ('MINUS', 'MUL', 'DIV'):
            # Require both to be numbers
            return isinstance(a, (int, float)) and isinstance(b, (int, float))
        elif operator in ('AND', 'OR'):
            # Require both to be booleans
            return isinstance(a, bool) and isinstance(b, bool)
        else:
            return True  # For comparisons, allow any types

    def _eval(self, node):
        if isinstance(node, Token):
            return node.value

        if isinstance(node, tuple):
            op, left, right = node

            # Handle unary negation
            if op.type == 'MINUS' and left is None:
                val = self._eval(right)
                if not isinstance(val, (int, float)):
                    raise TypeError(f"Cannot negate non-number: {val}")
                return -val

            # Handle logical NOT
            if op.type == 'NOT':
                operand = self._eval(right)
                if not isinstance(operand, bool):
                    raise TypeError(f"Cannot apply NOT to non-boolean: {operand}")
                return not operand

            left_val = self._eval(left) if left else None
            right_val = self._eval(right)

            # Type checks for operators
            if op.type in ('PLUS', 'MINUS', 'MUL', 'DIV', 'AND', 'OR'):
                if not self._are_compatible(left_val, right_val, op.type):
                    raise TypeError(
                        f"Unsupported operand types: {type(left_val)} and {type(right_val)} for operator {op.type}"
                    )

            # Perform operations
            if op.type == 'PLUS':
                return left_val + right_val
            elif op.type == 'MINUS':
                return left_val - right_val
            elif op.type == 'MUL':
                return left_val * right_val
            elif op.type == 'DIV':
                if right_val == 0:
                    raise ZeroDivisionError("Division by zero")
                return left_val / right_val
            elif op.type == 'EQ':
                return left_val == right_val
            elif op.type == 'NEQ':
                return left_val != right_val
            elif op.type == 'LT':
                return left_val < right_val
            elif op.type == 'GT':
                return left_val > right_val
            elif op.type == 'LTE':
                return left_val <= right_val
            elif op.type == 'GTE':
                return left_val >= right_val
            elif op.type == 'AND':
                return left_val and right_val
            elif op.type == 'OR':
                return left_val or right_val

        raise Exception(f"Unknown node: {node}")

evaluator_instance = Evaluator()

def evaluate(expression: str):
    scanner = Scanner(expression)
    parser = Parser(scanner)
    ast = parser.parse()
    return evaluator_instance.evaluate(ast)