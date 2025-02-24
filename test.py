import unittest
from main import calculate  # Changed import

class TestCalculator(unittest.TestCase):
    def test_basic_operations(self):
        self.assertAlmostEqual(calculate("1 - 2"), -1)
        self.assertAlmostEqual(calculate("3 + 5"), 8)
        self.assertAlmostEqual(calculate("6 * 4"), 24)  # Fixed
        self.assertAlmostEqual(calculate("8 / 2"), 4)  # Fixed

    def test_decimals(self):
        self.assertAlmostEqual(calculate("2.5 + 2.5 - 1.25"), 3.75)  # Fixed
        self.assertAlmostEqual(calculate("8.5 / 2"), 4.25)  # Fixed
        self.assertAlmostEqual(calculate(".5 * 2"), 1.0)  # Fixed

    def test_unary_negation(self):
        self.assertAlmostEqual(calculate("-3"), -3)  # Fixed
        self.assertAlmostEqual(calculate("--5"), 5)  # Fixed
        self.assertAlmostEqual(calculate("8.5 - -3"), 11.5)  # Fixed

    def test_parentheses(self):
        self.assertAlmostEqual(calculate("(10 * 2) / 5"), 4)  # Fixed
        self.assertAlmostEqual(calculate("(3 + 5) * 2"), 16)  # Fixed
        self.assertAlmostEqual(calculate("8.5 / (2 * 9)"), 8.5 / 18)  # Fixed

    def test_complex_expressions(self):
        self.assertAlmostEqual(calculate("8.5 / (2 * 9) - -3"), 8.5 / 18 + 3)  # Fixed
        self.assertAlmostEqual(calculate("(5 + 3) * -(-2 + 1)"), 8 * 1)  # Fixed

    def test_errors(self):
        with self.assertRaises(Exception):
            calculate("1 + abc")  # Fixed

        with self.assertRaises(Exception):
            calculate("5 / 0")  # Fixed

        with self.assertRaises(Exception):
            calculate("(3 + 5")  # Fixed

            # ----- New Tests for Stage 2 -----
    def test_boolean_comparisons(self):
                # Numeric comparisons
         self.assertTrue(calculate("5 < 10"))
         self.assertFalse(calculate("5 >= 10"))
         self.assertTrue(calculate("3.5 == 3.5"))
         self.assertTrue(calculate("2 != 3"))

    def test_boolean_operations(self):
                # Boolean equality
         self.assertTrue(calculate("true == true"))
         self.assertFalse(calculate("true != true"))
         self.assertTrue(calculate("false != true"))

                # Logical operators
         self.assertTrue(calculate("true and true"))
         self.assertFalse(calculate("true and false"))
         self.assertTrue(calculate("false or true"))
         self.assertFalse(calculate("false or false"))
         self.assertTrue(calculate("!(false)"))

    def test_mixed_expressions(self):
                # Comparisons with arithmetic
         self.assertTrue(calculate("(5 + 3) > (2 * 3)"))
         self.assertFalse(calculate("(10 / 2) <= 4"))

                # Boolean negation
         self.assertTrue(calculate("!(5 == 6)"))
         self.assertFalse(calculate("!(5 != 6)"))

    def test_type_mismatch_errors(self):
                # Disallow mixing numbers/booleans
         with self.assertRaises(Exception):
                    calculate("5 == true")  # Number vs Boolean

         with self.assertRaises(Exception):
                    calculate("true + 5")  # Boolean + Number

    if __name__ == "__main__":
            unittest.main()
