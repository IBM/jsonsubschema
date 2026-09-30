"""
Test suite for float/number type handling in JSON subschema checking.

This module tests floating-point number specific behaviors including:
- Float subtype relationships with exclusive and inclusive bounds
- Float multipleOf constraints and precision handling
- Number vs integer type distinctions
- Edge cases (empty ranges, single-point ranges, precision issues)

Created to improve test coverage of JSONTypeNumber class and float handling
in the jsonsubschema library.
"""

import unittest
from jsonschema.exceptions import SchemaError

from jsonsubschema import isSubschema


class TestFloatSubtypeRelationships(unittest.TestCase):
    """Test float subtype relationships with various bound configurations."""

    def test_float_exclusive_bounds_subtype(self):
        """Test that exclusive bounds create proper subtype relationship."""
        s1 = {
            "type": "number",
            "minimum": 5.0,
            "exclusiveMinimum": True,
            "maximum": 10.0,
            "exclusiveMaximum": True,
        }
        s2 = {"type": "number", "minimum": 5.0, "maximum": 10.0}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_very_small_floats(self):
        """Test subtyping with very small float values."""
        s1 = {"type": "number", "minimum": 0.0001, "maximum": 0.001}
        s2 = {"type": "number", "minimum": 0.0, "maximum": 0.01}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_very_large_floats(self):
        """Test subtyping with very large float values."""
        s1 = {"type": "number", "minimum": 1e10, "maximum": 1e11}
        s2 = {"type": "number", "minimum": 1e9, "maximum": 1e12}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_negative_floats_with_bounds(self):
        """Test subtyping with negative float bounds."""
        s1 = {"type": "number", "minimum": -10.5, "maximum": -5.5}
        s2 = {"type": "number", "minimum": -15.0, "maximum": -5.0}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_float_vs_integer_constraints(self):
        """Test float type with integer-valued constraints."""
        s1 = {"type": "number", "minimum": 5.0, "maximum": 10.0}
        s2 = {"type": "number", "minimum": 5, "maximum": 10}
        # These should be equivalent despite different numeric representation
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))


class TestFloatMultipleOf(unittest.TestCase):
    """Test multipleOf constraints with floating-point numbers."""

    def test_float_multipleOf_half(self):
        """Test multipleOf with 0.5 constraint."""
        s1 = {"type": "number", "multipleOf": 1.0}
        s2 = {"type": "number", "multipleOf": 0.5}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_float_multipleOf_decimal_precision(self):
        """Test multipleOf with 0.1 (tests decimal precision issues)."""
        s1 = {"type": "number", "multipleOf": 0.2}
        s2 = {"type": "number", "multipleOf": 0.1}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_float_multipleOf_rational(self):
        """Test multipleOf with rational number relationships."""
        s1 = {"type": "number", "multipleOf": 4.5}
        s2 = {"type": "number", "multipleOf": 1.5}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_negative_multipleOf_invalid(self):
        """Test that negative multipleOf is invalid."""
        s1 = {"type": "number", "multipleOf": 0.5}
        s2 = {"type": "number", "multipleOf": -0.5}
        self.assertRaises(SchemaError, isSubschema, s1, s2)

    def test_float_multipleOf_with_bounds(self):
        """Test multipleOf combined with min/max constraints."""
        s1 = {"type": "number", "multipleOf": 0.5, "minimum": 1.0, "maximum": 5.0}
        s2 = {"type": "number", "minimum": 0.0, "maximum": 10.0}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_float_multipleOf_with_integer_constraints(self):
        """Test float multipleOf that happens to be an integer."""
        s1 = {"type": "number", "multipleOf": 2.0}
        s2 = {"type": "number", "multipleOf": 1.0}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestNumberVsIntegerDistinction(unittest.TestCase):
    """Test the distinction between number and integer types."""

    def test_number_supertype_of_integer(self):
        """Test that number type is a supertype of integer type."""
        s1 = {"type": "integer"}
        s2 = {"type": "number"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_number_with_integer_constraints(self):
        """Test number type with constraints that match integer."""
        s1 = {"type": "number", "minimum": 5.5}
        s2 = {"type": "integer", "minimum": 6}
        # s1 allows 5.5, 5.6, ... which are not integers
        # s2 allows 6, 7, 8, ... which are all in s1's range
        # So s2 <: s1 (integer min 6 is subtype of number min 5.5)
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_number_multipleOf_one(self):
        """Test number with multipleOf 1.0 (integer equivalent multipleOf)."""
        s1 = {"type": "number", "multipleOf": 1.0}
        s2 = {"type": "integer"}
        # multipleOf 1.0 is considered integer-equivalent, so special handling applies
        # According to implementation, number with int-equiv multipleOf is subtype of integer
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_integer_multipleOf_vs_number_multipleOf(self):
        """Test integer multipleOf compared to number multipleOf."""
        s1 = {"type": "integer", "multipleOf": 2}
        s2 = {"type": "number", "multipleOf": 2.0}
        # Integer with multipleOf 2 is a subtype of number with multipleOf 2.0
        # And number with multipleOf 2.0 is also subtype of integer (int-equiv)
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_allOf_combining_integer_and_number(self):
        """Test allOf that combines integer and number constraints."""
        s1 = {"allOf": [{"type": "integer"}, {"type": "number", "minimum": 5.0}]}
        s2 = {"type": "integer", "minimum": 5}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))


class TestFloatEdgeCases(unittest.TestCase):
    """Test edge cases in float handling."""

    def test_empty_range_minimum_greater_than_maximum(self):
        """Test that min > max creates empty type (no valid values)."""
        s1 = {"type": "number", "minimum": 10.0, "maximum": 5.0}
        s2 = {"type": "number"}
        # Empty range is subtype of any number schema
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))

    def test_single_point_range(self):
        """Test range where min == max (single value)."""
        s1 = {"type": "number", "minimum": 7.5, "maximum": 7.5}
        s2 = {"type": "number", "minimum": 7.0, "maximum": 8.0}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_exclusive_single_point_range(self):
        """Test exclusive bounds that create empty range."""
        s1 = {
            "type": "number",
            "minimum": 5.0,
            "exclusiveMinimum": True,
            "maximum": 5.0,
            "exclusiveMaximum": True,
        }
        s2 = {"type": "number"}
        # Empty range (5.0 < x < 5.0 has no solutions)
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))

    def test_very_close_bounds(self):
        """Test bounds that are very close together."""
        s1 = {"type": "number", "minimum": 1.0, "maximum": 1.0001}
        s2 = {"type": "number", "minimum": 0.9999, "maximum": 1.0002}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestFloatMultipleOfAdvanced(unittest.TestCase):
    """Advanced multipleOf tests with floats."""

    def test_multipleOf_with_exclusive_bounds(self):
        """Test multipleOf combined with exclusive bounds."""
        s1 = {
            "type": "number",
            "multipleOf": 0.5,
            "minimum": 1.0,
            "exclusiveMinimum": True,
            "maximum": 5.0,
            "exclusiveMaximum": True,
        }
        s2 = {"type": "number", "minimum": 0.0, "maximum": 10.0}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_multipleOf_small_values(self):
        """Test multipleOf with very small values."""
        s1 = {"type": "number", "multipleOf": 0.01}
        s2 = {"type": "number", "multipleOf": 0.001}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_zero_multipleOf_invalid(self):
        """Test that multipleOf 0 is invalid."""
        s1 = {"type": "number", "multipleOf": 0}
        s2 = {"type": "number"}
        self.assertRaises(SchemaError, isSubschema, s1, s2)


if __name__ == "__main__":
    unittest.main()
