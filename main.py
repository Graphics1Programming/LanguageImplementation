from scanner import Scanner
from parser import Parser
from evaluator import Evaluator
import os

# Create one Evaluator instance globally to preserve variable state
evaluator_instance = Evaluator()

def clear_screen():
    """Clear the terminal screen, works on Windows and Unix."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("[Screen cleared]")

def calculate(text):
    """
    Process input text by scanning, parsing, and evaluating it.
    Returns the evaluated result or raises an appropriate exception.
    """
    try:
        scanner = Scanner(text)          # Tokenize the input text
        parser = Parser(scanner)         # Parse tokens into an abstract syntax tree (AST)
        ast = parser.parse()             # Generate the AST
        # Evaluate the AST using the global evaluator instance
        return evaluator_instance.evaluate(ast)
    except TypeError as te:
        raise Exception(f"Type mismatch error: {te}")
    except SyntaxError as se:
        raise Exception(f"Syntax error: {se}")
    except ValueError as ve:
        raise Exception(f"Value error: {ve}")
    except Exception as ex:
        # General catch-all for unexpected errors during calculation
        raise Exception(f"Error while calculating expression: {ex}")

def format_result(value):
    """
    Format evaluated values for user-friendly output.
    - Strings are quoted
    - Booleans are lowercase 'true' or 'false'
    - Other types are converted to string directly
    """
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    else:
        return str(value)

if __name__ == "__main__":
    import sys

    # No command-line arguments: start interactive REPL mode
    if len(sys.argv) == 1:
        print("Enter expressions (type 'exit' or 'quit' to stop, 'clear' to clear screen)")
        while True:
            try:
                user_input = input(">>> ").strip()
                if not user_input:
                    continue

                # Exit commands
                if user_input.lower() in ('exit', 'quit'):
                    print("Exiting...")
                    break

                # Clear screen command
                if user_input.lower() == 'clear':
                    clear_screen()
                    continue

                try:
                    result = calculate(user_input)
                    if result is not None:
                        formatted = format_result(result)
                        print(f"Result: {formatted}")
                except Exception as error:
                    print(f"Error: {error}")

            except KeyboardInterrupt:
                # Ignore Ctrl+C (do not exit)
                print("\nKeyboardInterrupt ignored. Use 'exit' or 'quit' to stop.")

    # One command-line argument: treat as filename and execute line-by-line
    elif len(sys.argv) == 2:
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        try:
                            result = calculate(line)
                            if result is not None:
                                formatted = format_result(result)
                                print(f"{line} = {formatted}")
                        except KeyboardInterrupt:
                            print("\nExecution interrupted by user.")
                            break
                        except Exception as error:
                            print(f"Error: {error}")
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found")

    else:
        print("Usage: python main.py [input_file]")
