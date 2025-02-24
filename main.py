from scanner import Scanner
from parser import Parser
from evaluator import Evaluator

def calculate(text):
    scanner = Scanner(text)
    parser = Parser(scanner)
    ast = parser.parse()
    return Evaluator().evaluate(ast)

if __name__ == "__main__":
    import sys

    # Interactive mode if no arguments
    if len(sys.argv) == 1:
        print("Enter expressions (Ctrl+C to exit)")
        while True:
            try:
                text = input(">>> ").strip()
                if text:
                    try:
                        result = calculate(text)
                        print(f"Result: {result}")
                    except Exception as e:
                        print(f"Error: {e}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break

    # File mode if argument provided
    elif len(sys.argv) == 2:
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            result = calculate(line)
                            print(f"{line} = {result}")
                        except Exception as e:
                            print(f"Error: {e}")
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found")

    else:
        print("Usage: python main.py [input_file]")