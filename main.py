from scanner import Scanner
from parser import Parser
from evaluator import Evaluator

evaluator = Evaluator()

def calculate(text):
    try:
        scanner = Scanner(text)
        parser = Parser(scanner)
        ast = parser.parse()
        return evaluator.evaluate(ast)
    except TypeError as te:
        raise Exception(f"Type mismatch error: {te}")
    except SyntaxError as se:
        raise Exception(f"Syntax error: {se}")
    except ValueError as ve:
        raise Exception(f"Value error: {ve}")
    except ZeroDivisionError as zde:
        raise Exception(f"Math error: {zde}")
    except KeyboardInterrupt:
        raise
    except Exception as ex:
        raise Exception(f"Error while calculating expression: {ex}")

def format_result(value):
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return 'true' if value else 'false'
    else:
        return str(value)

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        print("Enter expressions (Ctrl+C to exit)")
        while True:
            try:
                user_input = input(">>> ").strip()
                if user_input:
                    try:
                        result = calculate(user_input)
                        print(f"Result: {format_result(result)}")
                    except KeyboardInterrupt:
                        raise
                    except Exception as error:
                        print(f"Error: {error}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

    elif len(sys.argv) == 2:
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            result = calculate(line)
                            print(f"{line} = {format_result(result)}")
                        except KeyboardInterrupt:
                            print("\nExecution interrupted by user.")
                            break
                        except Exception as error:
                            print(f"Error: {error}")
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found")

    else:
        print("Usage: python main.py [input_file]")
