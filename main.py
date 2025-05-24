from scanner import Scanner
from parser import Parser
from evaluator import Evaluator
import os

# Global Evaluator instance to retain variable states across expressions
evaluator_instance = Evaluator()


def clear_screen():
    """
    Clears the terminal screen.
    Supports both Windows ('cls') and Unix/Linux/Mac ('clear').
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    print("[Screen cleared]")


def calculate(text):
    """
    Performs the complete process of evaluating an input expression.

    Steps:
    1. Tokenize the input using Scanner
    2. Parse tokens into an AST using Parser
    3. Evaluate the AST using Evaluator

    Parameters:
    - text (str): The user input expression

    Returns:
    - The result of evaluation (any data type)

    Raises:
    - Exception: With appropriate error message if any stage fails
    """
    try:
        scanner = Scanner(text)
        parser = Parser(scanner)
        ast = parser.parse()
        return evaluator_instance.evaluate(ast)
    except TypeError as te:
        raise Exception(f"Type mismatch error: {te}")
    except SyntaxError as se:
        raise Exception(f"Syntax error: {se}")
    except ValueError as ve:
        raise Exception(f"Value error: {ve}")
    except Exception as ex:
        raise Exception(f"Error while calculating expression: {ex}")


def format_result(value):
    """
    Formats the result value into a user-friendly string.

    Parameters:
    - value (any): The result from evaluation

    Returns:
    - str: Formatted string
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    else:
        return str(value)


def read_multiline_input(prompt=">>> "):
    """
    Reads multi-line input from the user.
    Continues reading until all braces are matched.

    Parameters:
    - prompt (str): The prompt string to display

    Returns:
    - str: Combined multi-line input
    """
    lines = []
    open_braces = 0
    while True:
        line = input(prompt)
        lines.append(line)
        open_braces += line.count("{") - line.count("}")
        if open_braces <= 0 and line.strip() != "":
            break
        prompt = "... "
    return "\n".join(lines)


if __name__ == "__main__":
    import sys

    # Interactive Mode: No command-line arguments
    if len(sys.argv) == 1:
        print("Enter expressions (type 'exit' or 'quit' to stop, 'clear' to clear screen)")
        while True:
            try:
                user_input = read_multiline_input().strip()
                if not user_input:
                    continue

                # Handle special commands
                if user_input.lower() in ('exit', 'quit'):
                    print("Exiting...")
                    break
                if user_input.lower() == 'clear':
                    clear_screen()
                    continue

                # Process and display result
                try:
                    result = calculate(user_input)
                    if result is not None:
                        formatted = format_result(result)
                        print(f"Result: {formatted}")
                except Exception as error:
                    print(f"Error: {error}")

            except KeyboardInterrupt:
                # Prevent exiting on Ctrl+C
                print("\nKeyboardInterrupt ignored. Use 'exit' or 'quit' to stop.")

    # Script Mode: One argument passed (input file)
    elif len(sys.argv) == 2:
        try:
            with open(sys.argv[1]) as f:
                text = f.read()
                try:
                    result = calculate(text)
                    if result is not None:
                        formatted = format_result(result)
                        print(f"Result: {formatted}")
                except Exception as error:
                    print(f"Error: {error}")
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found")

    # Invalid usage
    else:
        print("Usage: python main.py [input_file]")
