import unittest
from main import calculate
class TestCalculator(unittest.TestCase):
    # ===== Stage 1 Tests =====
    def test_basic_operations(self):
        self.assertAlmostEqual(calculate("1 - 2"), -1)
        self.assertAlmostEqual(calculate("3 + 5"), 8)
        self.assertAlmostEqual(calculate("6 * 4"), 24)
        self.assertAlmostEqual(calculate("8 / 2"), 4)

    def test_decimals(self):
        self.assertAlmostEqual(calculate("2.5 + 2.5 - 1.25"), 3.75)
        self.assertAlmostEqual(calculate("8.5 / 2"), 4.25)
        self.assertAlmostEqual(calculate(".5 * 2"), 1.0)

    def test_unary_negation(self):
        self.assertAlmostEqual(calculate("-3"), -3)
        self.assertAlmostEqual(calculate("--5"), 5)
        self.assertAlmostEqual(calculate("8.5 - -3"), 11.5)

    def test_parentheses(self):
        self.assertAlmostEqual(calculate("(10 * 2) / 5"), 4)
        self.assertAlmostEqual(calculate("(3 + 5) * 2"), 16)
        self.assertAlmostEqual(calculate("8.5 / (2 * 9)"), 8.5 / 18)

    def test_complex_expressions(self):
        self.assertAlmostEqual(calculate("8.5 / (2 * 9) - -3"), 8.5 / 18 + 3)
        self.assertAlmostEqual(calculate("(5 + 3) * -(-2 + 1)"), 8 * 1)

    def test_errors(self):
        with self.assertRaises(Exception):
            calculate("1 + abc")

        with self.assertRaises(Exception):
            calculate("5 / 0")

        with self.assertRaises(Exception):
            calculate("(3 + 5")

    # ===== Stage 2 Tests =====
    def test_boolean_comparisons(self):
        self.assertTrue(calculate("5 < 10"))
        self.assertFalse(calculate("5 >= 10"))
        self.assertTrue(calculate("3.5 == 3.5"))
        self.assertTrue(calculate("2 != 3"))

    def test_boolean_operations(self):
        self.assertTrue(calculate("true == true"))
        self.assertFalse(calculate("true != true"))
        self.assertTrue(calculate("false != true"))
        self.assertTrue(calculate("true and true"))
        self.assertFalse(calculate("true and false"))
        self.assertTrue(calculate("false or true"))
        self.assertFalse(calculate("false or false"))
        self.assertTrue(calculate("!(false)"))

    def test_mixed_expressions(self):
        self.assertTrue(calculate("(5 + 3) > (2 * 3)"))
        self.assertFalse(calculate("(10 / 2) <= 4"))
        self.assertTrue(calculate("!(5 == 6)"))
        self.assertFalse(calculate("!(5 != 6)"))

    def test_type_mismatch_errors(self):
        with self.assertRaises(Exception):
            calculate("true + 5")

        with self.assertRaises(Exception):
            calculate("5 + \"1\"")  # Number + String

    # ===== Stage 3 Tests =====
    def test_string_operations(self):
        # Concatenation
        self.assertEqual(calculate("\"hello\" + \" \" + \"world\""), "hello world")
        self.assertEqual(calculate("\"foo\" + \"bar\""), "foobar")

        # Equality
        self.assertTrue(calculate("\"foo\" + \"bar\" == \"foobar\""))
        self.assertTrue(calculate("\"10 corgis\" != \"10\" + \"corgis\""))

        # Type safety
        self.assertFalse(calculate("\"5\" == 5"))  # String vs Number
        self.assertFalse(calculate("\"true\" == true"))  # String vs Boolean

        # String comparisons (lexicographical order)
        self.assertTrue(calculate("\"apple\" < \"banana\""))
        self.assertTrue(calculate("\"zebra\" > \"apple\""))
        self.assertTrue(calculate("\"cat\" <= \"cat\""))
        self.assertFalse(calculate("\"dog\" >= \"elephant\""))

    def test_empty_strings(self):
        self.assertEqual(calculate("\"\" + \"\""), "")  # Empty concatenation
        self.assertTrue(calculate("\"\" == \"\""))  # Empty equality
        self.assertFalse(calculate("\"\" != \"\""))

    def test_string_type_mismatch(self):
        with self.assertRaises(Exception):
            calculate("\"text\" + 5")  # String + Number

        with self.assertRaises(Exception):
            calculate("\"text\" - \"t\"")  # Invalid string operation


if __name__ == "__main__":
    unittest.main()