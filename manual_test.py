from scanner import Scanner
from main import calculate, format_result  # Import formatting helper


def show_tokens(text):
    scanner = Scanner(text)
    tokens = []
    try:
        while True:
            token = scanner.get_next_token()
            if token.type == 'EOF':
                break
            tokens.append(str(token))  # Uses Token's __str__ method
        print("\nTokens:", " → ".join(tokens))
        return True
    except Exception as e:
        print(f"\nTokenization Error: {str(e)}")
        return False


def main():
    print("Interactive Calculator (type 'exit' to quit)")
    while True:
        try:
            text = input("\n>>> ").strip()
            if text.lower() == 'exit':
                break

            if not text:
                continue

            # Show tokenization first
            tokenization_ok = show_tokens(text)
            if not tokenization_ok:
                continue

            # Then show evaluation
            try:
                result = calculate(text)
                formatted = format_result(result)  # Use formatting helper
                print(f"Result: {formatted}")
            except Exception as e:
                print(f"Evaluation Error: {str(e)}")

        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()