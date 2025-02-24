from lexer import Lexer
from main import evaluate_expression


def show_scanner_output(text):
    lexer = Lexer(text)
    tokens = []
    try:
        while True:
            token = lexer.get_next_token()
            if token.type == 'EOF':
                break
            tokens.append(str(token))  # Use __str__ representation
        print("\nScanner Output:")
        print(" → ".join(tokens))
        return True
    except Exception as e:
        print(f"\nScanner Error: {str(e)}")
        return False


def main():
    while True:
        user_input = input("\nEnter expression (type 'exit' to quit): ").strip()
        if user_input.lower() == 'exit':
            break

        if not user_input:
            continue

        # First show scanner output
        valid = show_scanner_output(user_input)
        if not valid:
            continue

        # Then show evaluation result
        try:
            result = evaluate_expression(user_input)
            print(f"Evaluation Result: {result}")
        except Exception as e:
            print(f"Evaluation Error: {str(e)}")


if __name__ == "__main__":
    main()