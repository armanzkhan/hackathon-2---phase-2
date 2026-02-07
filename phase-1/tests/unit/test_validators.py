"""
Unit tests for validation functions.

Tests input validation for titles, IDs, and descriptions.
"""

import unittest
from src.validation.validators import validate_title, validate_id, validate_description


class TestValidators(unittest.TestCase):
    """Test suite for validation functions."""

    def test_validate_title_with_valid_input(self):
        """T019 [US1]: validate_title() should accept valid titles."""
        is_valid, error = validate_title("Buy groceries")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_title_with_empty_input(self):
        """T020 [US1]: validate_title() should reject empty title."""
        is_valid, error = validate_title("")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())

    def test_validate_title_with_whitespace_only(self):
        """Additional test: validate_title() should reject whitespace-only."""
        is_valid, error = validate_title("   ")
        self.assertFalse(is_valid)
        self.assertIn("empty", error.lower())

    def test_validate_title_with_tabs_and_newlines(self):
        """Additional test: validate_title() should reject tabs/newlines only."""
        is_valid, error = validate_title("\t\n")
        self.assertFalse(is_valid)

    def test_validate_title_strips_whitespace(self):
        """Additional test: validate_title() should accept title with leading/trailing spaces."""
        is_valid, error = validate_title("  Valid Title  ")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")

    def test_validate_title_with_single_character(self):
        """Additional test: validate_title() should accept single character."""
        is_valid, error = validate_title("A")
        self.assertTrue(is_valid)

    def test_validate_id_with_valid_positive_integer(self):
        """Additional test: validate_id() should accept positive integers."""
        is_valid, parsed_id, error = validate_id("1")
        self.assertTrue(is_valid)
        self.assertEqual(parsed_id, 1)
        self.assertEqual(error, "")

        is_valid, parsed_id, error = validate_id("42")
        self.assertTrue(is_valid)
        self.assertEqual(parsed_id, 42)

    def test_validate_id_with_non_numeric_input(self):
        """Additional test: validate_id() should reject non-numeric input."""
        is_valid, parsed_id, error = validate_id("abc")
        self.assertFalse(is_valid)
        self.assertEqual(parsed_id, 0)
        self.assertIn("invalid", error.lower())

    def test_validate_id_with_negative_number(self):
        """Additional test: validate_id() should reject negative numbers."""
        is_valid, parsed_id, error = validate_id("-5")
        self.assertFalse(is_valid)
        self.assertIn("positive", error.lower())

    def test_validate_id_with_zero(self):
        """Additional test: validate_id() should reject zero."""
        is_valid, parsed_id, error = validate_id("0")
        self.assertFalse(is_valid)
        self.assertIn("positive", error.lower())

    def test_validate_id_with_float(self):
        """Additional test: validate_id() should reject floats."""
        is_valid, parsed_id, error = validate_id("1.5")
        self.assertFalse(is_valid)

    def test_validate_id_with_whitespace(self):
        """Additional test: validate_id() should strip whitespace."""
        is_valid, parsed_id, error = validate_id("  123  ")
        self.assertTrue(is_valid)
        self.assertEqual(parsed_id, 123)

    def test_validate_id_with_leading_zeros(self):
        """Additional test: validate_id() should handle leading zeros."""
        is_valid, parsed_id, error = validate_id("007")
        self.assertTrue(is_valid)
        self.assertEqual(parsed_id, 7)

    def test_validate_description_accepts_any_string(self):
        """Additional test: validate_description() should accept any string."""
        is_valid, error = validate_description("")
        self.assertTrue(is_valid)
        self.assertEqual(error, "")

        is_valid, error = validate_description("Any text")
        self.assertTrue(is_valid)

        is_valid, error = validate_description("Very long text" * 1000)
        self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()
