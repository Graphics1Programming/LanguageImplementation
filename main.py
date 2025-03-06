from scanner import Scanner
from parser import Parser
from evaluator import Evaluator

def calculate(text):
    try:
        scanner = Scanner(text)
        parser = Parser(scanner)
        ast = parser.parse()
        return Evaluator().evaluate(ast)
    except TypeError as te:  # Renamed to 'te'
        raise Exception(f"Type mismatch error: {te}")
    except SyntaxError as se:  # Renamed to 'se'
        raise Exception(f"Syntax error: {se}")
    except ValueError as ve:  # Renamed to 've'
        raise Exception(f"Value error: {ve}")
    except Exception as ex:  # Renamed to 'ex'
        raise Exception(f"Error while calculating expression: {ex}")

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
                user_input = input(">>> ").strip()
                if user_input:
                    try:
                        result = calculate(user_input)
                        formatted = format_result(result)
                        print(f"Result: {formatted}")
                    except Exception as error:  # Renamed to 'error'
                        print(f"Error: {error}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

    # File mode
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
                        except Exception as error:  # Renamed to 'error'
                            print(f"Error: {error}")
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found")

    else:
        print("Usage: python main.py [input_file]")