import unittest
from io import StringIO
import sys
from evaluator import evaluate  # Make sure evaluator.py has an `evaluate()` function

class TestStage1Arithmetic(unittest.TestCase):
    def test_subtraction(self):
        self.assertEqual(evaluate("1 - 2"), -1)

    def test_floating_add_sub(self):
        self.assertAlmostEqual(evaluate("2.5 + 2.5 - 1.25"), 3.75)

    def test_parentheses_and_division(self):
        self.assertEqual(evaluate("(10 * 2) / 6"), (10 * 2) / 6)

    def test_unary_negation(self):
        self.assertAlmostEqual(evaluate("8.5 / (2 * 9) - -3"), (8.5 / (2 * 9)) + 3)


class TestStage2Boolean(unittest.TestCase):
    def test_boolean_equality(self):
        self.assertEqual(evaluate("true == false"), False)
        self.assertEqual(evaluate("true != false"), True)

    def test_numeric_comparison(self):
        self.assertEqual(evaluate("5 < 10"), True)
        self.assertEqual(evaluate("5 > 10"), False)

    def test_combined_boolean_logic(self):
        self.assertEqual(evaluate("!(5 - 4 > 3 * 2 == !false)"), True)

    def test_logical_and_or(self):
        self.assertEqual(evaluate("true and true"), True)
        self.assertEqual(evaluate("false and true"), False)
        self.assertEqual(evaluate("(0 < 1) or false"), True)
        self.assertEqual(evaluate("false or false"), False)


class TestStage3Text(unittest.TestCase):
    def test_basic_concatenation(self):
        self.assertEqual(evaluate('"hello" + " " + "world"'), "hello world")

    def test_text_equality(self):
        self.assertEqual(evaluate('"foo" + "bar" == "foobar"'), True)

    def test_text_inequality(self):
        self.assertEqual(evaluate('"10 corgis" != "10" + "corgis"'), True)

    def test_mixed_type_decision(self):
        with self.assertRaises(TypeError):
            evaluate('1 + "0"')

        with self.assertRaises(TypeError):
            evaluate('false == "false"')


class TestStage4Print(unittest.TestCase):
    def test_print_number(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        evaluate("print(5 + 3)")
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "8")

    def test_print_boolean(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        evaluate("print(true and false)")
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "False")

    def test_print_text(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        evaluate('print("hello " + "world")')
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "hello world")

    def test_print_nested_expression(self):
        captured_output = StringIO()
        sys.stdout = captured_output
        evaluate('print((2 + 3) * (1 + 1))')
        sys.stdout = sys.__stdout__
        self.assertEqual(captured_output.getvalue().strip(), "10")


if __name__ == "__main__":
    unittest.main()
