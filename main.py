from scanner import Scanner
from parser import Parser  # Ensure renamed parser file
from evaluator import Evaluator

def calculate(text):  # This parameter is fine
    try:
        scanner = Scanner(text)
        parser = Parser(scanner)
        ast = parser.parse()
        return Evaluator().evaluate(ast)
    except TypeError as e:
        raise Exception(f"Type mismatch error: {e}")
    except SyntaxError as e:
        raise Exception(f"Syntax error: {e}")
    except ValueError as e:
        raise Exception(f"Value error: {e}")
    except Exception as e:
        raise Exception(f"Error while calculating expression: {e}")

def format_result(value):
    """Format values for clear output"""
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    else:
        return str(value)

if __name__ == "__main__":
    import sys

    # Interactive mode if no arguments
    if len(sys.argv) == 1:
        print("Enter expressions (Ctrl+C to exit)")
        while True:
            try:
                # Changed variable name from 'text' to 'user_input'
                user_input = input(">>> ").strip()
                if user_input:
                    try:
                        result = calculate(user_input)
                        formatted = format_result(result)
                        print(f"Result: {formatted}")
                    except Exception as e:
                        print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

    # File mode remains unchanged
    elif len(sys.argv) == 2:
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            result = calculate(line)
                            formatted = format_result(result)
                            print(f"{line} = {formatted}")
                        except Exception as e:
                            print(f"Error: {e}")
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found")

    else:
        print("Usage: python main.py [input_file]")
