from scanner import Scanner
from parser import Parser
from evaluator import Evaluator
from tokens import Token


def main():
    # Example inputs
    input_text = '3 + 5 * (2 - 1) == true'
    print("Input Expression:", input_text)

    # Initialize Scanner
    scanner = Scanner(input_text)

    # Tokenize the input
    tokens = []
    token = scanner.get_next_token()
    while token.type != 'EOF':
        tokens.append(token)
        token = scanner.get_next_token()

    print("Tokens:", tokens)

    # Initialize Parser
    parser = Parser(tokens)

    # Parse the expression
    ast = parser.parse()
    print("Abstract Syntax Tree (AST):", ast)

    # Initialize Evaluator
    evaluator = Evaluator()

    # Evaluate the AST
    result = evaluator.evaluate(ast)
    print("Result:", result)


if __name__ == "__main__":
    main()
