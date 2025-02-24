from lexer import Lexer
from parser import Parser
from evaluator import Evaluator

def evaluate_expression(text):
    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse()
    evaluator = Evaluator()
    return evaluator.visit(ast)

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        return

    with open(sys.argv[1], 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    result = evaluate_expression(line)
                    print(f"{line} = {result}")
                except Exception as e:
                    print(f"Error evaluating '{line}': {str(e)}")

if __name__ == "__main__":
    main()