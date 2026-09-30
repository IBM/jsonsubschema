"""
Test suite for edge cases in JSON subschema checking.

This module tests edge cases including:
- Empty schemas and bot types
- Deep nesting and recursion limits
- Boundary values (empty arrays, empty objects, empty strings)
- Schema combinations with allOf, anyOf, oneOf, not
- Type combinations and edge cases

Created to improve test coverage of edge case handling.
"""

import unittest

from jsonsubschema import isSubschema


class TestEmptySchemas(unittest.TestCase):
    """Test empty and trivial schemas."""

    def test_empty_schema_is_top(self):
        """Test empty schema {} accepts all values (top type)."""
        s1 = {"type": "string"}
        s2 = {}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_not_empty_object(self):
        """Test not empty object is very restrictive (accepts nothing)."""
        s1 = {"not": {}}
        s2 = {"type": "string"}
        # not {} accepts nothing (since {} accepts everything)
        # So not {} is a subtype of any schema
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        # String type accepts values, so not subtype of impossible schema
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestBoundaryValues(unittest.TestCase):
    """Test boundary value constraints."""

    def test_empty_array(self):
        """Test array with zero items."""
        s1 = {"type": "array", "minItems": 0, "maxItems": 0}
        s2 = {"type": "array"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_empty_object(self):
        """Test object with zero properties."""
        s1 = {"type": "object", "minProperties": 0, "maxProperties": 0}
        s2 = {"type": "object"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_empty_string(self):
        """Test string with zero length."""
        s1 = {"type": "string", "minLength": 0, "maxLength": 0}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_zero_number(self):
        """Test number range containing only zero."""
        s1 = {"type": "number", "minimum": 0, "maximum": 0}
        s2 = {"type": "number"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestAllOfCombinations(unittest.TestCase):
    """Test allOf schema combinations."""

    def test_allOf_redundant(self):
        """Test allOf with redundant constraints."""
        s1 = {"allOf": [{"type": "integer"}, {"type": "integer"}]}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_allOf_overlapping_ranges(self):
        """Test allOf with overlapping number ranges."""
        s1 = {
            "allOf": [
                {"type": "integer", "minimum": 0},
                {"type": "integer", "maximum": 100},
            ]
        }
        s2 = {"type": "integer", "minimum": 0, "maximum": 100}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_allOf_disjoint_types(self):
        """Test allOf with disjoint types creates bot (empty set)."""
        # allOf with disjoint types creates an impossible schema
        s1 = {"allOf": [{"type": "string"}, {"type": "integer"}]}
        # This schema accepts nothing, so it's a subtype of any schema
        s2 = {"type": "string"}
        # s1 is a subtype of any schema (including s2) because it accepts nothing
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        # But s2 is not a subtype of s1 because s2 accepts values while s1 accepts nothing
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_allOf_nested(self):
        """Test nested allOf."""
        s1 = {"allOf": [{"allOf": [{"type": "integer"}]}]}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))


class TestAnyOfCombinations(unittest.TestCase):
    """Test anyOf schema combinations."""

    def test_anyOf_single(self):
        """Test anyOf with single schema."""
        s1 = {"anyOf": [{"type": "string"}]}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_anyOf_union(self):
        """Test anyOf creates union type."""
        s1 = {"type": "string"}
        s2 = {"anyOf": [{"type": "string"}, {"type": "integer"}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_anyOf_subset(self):
        """Test anyOf where one is subset of another."""
        s1 = {"anyOf": [{"type": "integer", "minimum": 0}]}
        s2 = {"anyOf": [{"type": "integer"}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_anyOf_nested(self):
        """Test nested anyOf."""
        s1 = {"anyOf": [{"anyOf": [{"type": "string"}]}]}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))


class TestOneOfCombinations(unittest.TestCase):
    """Test oneOf schema combinations."""

    def test_oneOf_single(self):
        """Test oneOf with single schema."""
        s1 = {"oneOf": [{"type": "string"}]}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_oneOf_disjoint(self):
        """Test oneOf with disjoint types."""
        s1 = {"type": "string"}
        s2 = {"oneOf": [{"type": "string"}, {"type": "integer"}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_oneOf_overlapping_becomes_disjoint(self):
        """Test oneOf with overlapping schemas (values in both fail oneOf)."""
        s1 = {
            "oneOf": [
                {"type": "integer", "minimum": 0},
                {"type": "integer", "maximum": 10},
            ]
        }
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestNotCombinations(unittest.TestCase):
    """Test not keyword combinations."""

    def test_not_not_identity(self):
        """Test double negation."""
        s1 = {"not": {"not": {"type": "string"}}}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_not_with_type(self):
        """Test not with specific type."""
        s1 = {"not": {"type": "string"}}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))


class TestEnumEdgeCases(unittest.TestCase):
    """Test enum with edge cases."""

    def test_enum_single_value(self):
        """Test enum with single value."""
        s1 = {"enum": ["value"]}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_enum_subset(self):
        """Test enum subset relationship."""
        s1 = {"enum": [1, 2]}
        s2 = {"enum": [1, 2, 3, 4]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_enum_with_type(self):
        """Test enum combined with type."""
        s1 = {"type": "integer", "enum": [1, 2, 3]}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestMultipleTypes(unittest.TestCase):
    """Test schemas with multiple types."""

    def test_type_array_single(self):
        """Test type array with single element."""
        s1 = {"type": ["string"]}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_type_array_subset(self):
        """Test type array subset."""
        s1 = {"type": ["string"]}
        s2 = {"type": ["string", "integer"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_type_array_all_types(self):
        """Test type array with all JSON types."""
        s1 = {
            "type": [
                "string",
                "number",
                "integer",
                "boolean",
                "null",
                "array",
                "object",
            ]
        }
        s2 = {}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_type_array_with_constraints(self):
        """Test type array with constraints on one type."""
        s1 = {"type": ["string", "integer"], "minimum": 10}
        s2 = {"type": ["string", "integer"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


if __name__ == "__main__":
    unittest.main()
