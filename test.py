import unittest
from main import evaluate_expression


class TestCalculator(unittest.TestCase):
    def test_basic_operations(self):
        self.assertAlmostEqual(evaluate_expression("1 - 2"), -1)
        self.assertAlmostEqual(evaluate_expression("3 + 5"), 8)
        self.assertAlmostEqual(evaluate_expression("6 * 4"), 24)
        self.assertAlmostEqual(evaluate_expression("8 / 2"), 4)

    def test_decimals(self):
        self.assertAlmostEqual(evaluate_expression("2.5 + 2.5 - 1.25"), 3.75)
        self.assertAlmostEqual(evaluate_expression("8.5 / 2"), 4.25)
        self.assertAlmostEqual(evaluate_expression(".5 * 2"), 1.0)

    def test_unary_negation(self):
        self.assertAlmostEqual(evaluate_expression("-3"), -3)
        self.assertAlmostEqual(evaluate_expression("--5"), 5)
        self.assertAlmostEqual(evaluate_expression("8.5 - -3"), 11.5)

    def test_parentheses(self):
        self.assertAlmostEqual(evaluate_expression("(10 * 2) / 5"), 4)
        self.assertAlmostEqual(evaluate_expression("(3 + 5) * 2"), 16)
        self.assertAlmostEqual(evaluate_expression("8.5 / (2 * 9)"), 8.5 / 18)

    def test_complex_expressions(self):
        self.assertAlmostEqual(evaluate_expression("8.5 / (2 * 9) - -3"), 8.5 / 18 + 3)
        self.assertAlmostEqual(evaluate_expression("(5 + 3) * -(-2 + 1)"), 8 * 1)

    def test_errors(self):
        with self.assertRaises(Exception):
            evaluate_expression("1 + abc")  # Invalid characters

        with self.assertRaises(Exception):
            evaluate_expression("5 / 0")  # Division by zero

        with self.assertRaises(Exception):
            evaluate_expression("(3 + 5")  # Mismatched parentheses


if __name__ == "__main__":
    unittest.main()