from scanner import Scanner
from main import calculate


def show_tokens(text):
    scanner = Scanner(text)
    tokens = []
    try:
        while True:
            token = scanner.get_next_token()
            if token.type == 'EOF': break
            tokens.append(str(token))  # Uses Token's __str__ method
        print("\nTokens:", " → ".join(tokens))
    except Exception as e:
        print(f"Token Error: {e}")
        return False
    return True


def main():
    while True:
        text = input("\nEnter expression (exit to quit): ").strip()
        if text.lower() == 'exit': break

        if show_tokens(text):  # Show tokenization first
            try:
                result = calculate(text)
                print(f"Result: {result}")
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()