Mini Language Interpreter

A small programming language interpreter built using Python 3.13. It supports variable assignments, basic arithmetic calculations, boolean logic, and text values. The interpreter manages a global data store for variables and offers full control flow features including nested if-else statements and while loops. Programs can be run line-by-line or from a script file.

Project Structure

The project is organised under the folder LDesign (for example, in PyCharm at C:/Users/ldi/PycharmProjects/LDesign) and contains the following key files:

- main.py — The entry point to run the interpreter either interactively or with a script file like input.txt.
- evaluator.py — Contains the core logic to evaluate the parsed abstract syntax tree (AST), including variable management, control flow, and operations.
- tokens.py — Defines token types used by the scanner and parser.
- scanner.py — Tokenises the input source code into tokens.
- parser.py — Parses tokens into an AST representing the program structure.
- data.py — Manages the global storage for variables.
- input.txt — An example script file containing code to be executed by the interpreter.

Features

- Variables: Create, assign, and use values globally.
- Basic calculations: Addition, subtraction, multiplication, division, modulus.
- Boolean logic: and, or, not operations.
- Text handling: String values and concatenation.
- Control flow: Supports nested if, else if, else blocks and while loops with break and continue support.
- Built-in functions: input(), print(), int() for type conversion.
- Variable deletion: del variable_name.
- Shell commands: clear (clear screen), exit and quit (stop interpreter).
- Multi-line blocks: Write multi-line logic with {} braces.
- Script execution: Run programs from files like input.txt, examples.txt.

Brief Description of Language Syntax

This mini-language uses a simple, Python-like syntax designed for easy learning and execution:

- Blocks: Use curly braces { ... } to group multiple statements in control structures such as if, else if, else, and while.

- Variables: Dynamically typed, declared by assignment. Examples:
  x = 10
  message = "Hello, world"

- Comments: Single-line comments start with #.

- Control Flow: Nested conditional statements with if, else if, and else:

if (x > 0) {
    if (x < 20) {
        print("x is between 1 and 19")
    } else if (x == 20) {
        print("x is exactly 20")
    } else {
        print("x is greater than 20")
    }
} else {
    print("x is zero or negative")
}

- Loops: Use while with conditions; supports break to exit early:

while (x > 0) {
    print(x)
    x = x - 1
    if (x == 2) {
        break
    }
}

- Operators: Arithmetic (+, -, *, /, %), comparison (==, !=, <, >, <=, >=), and logical (and, or, not) operators.

Built-in Functions

- print(expression) — display output
- input(prompt) — read user input
- int(expression) — convert to integer
- del variable — delete a variable

Example Programs

The repository includes five example files, each demonstrating important aspects of the language.

These can run example scripts named example1.txt through example5.txt by configuring and running the interpreter via the main.py file.

How to Start

Requirements:
- Python 3.13 installed on your system.

Installation and Running:

1. Clone the repository:
git clone https://github.com/Graphics1Programming/LanguageImplementation.git

2. Navigate to the project folder (example path):
cd C:/Users/ldi/PycharmProjects/LDesign

3. Run the interpreter interactively:
python main.py

4. Or run a script file, for example:
python main.py example1.txt

Replace example1.txt with example2.txt, example3.txt, etc., to run other examples.
