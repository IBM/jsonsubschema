"""
Test suite for performance edge cases.

This module tests performance-related scenarios including:
- Large schemas with many properties
- Deeply nested schemas
- Large enum values
- Large array constraints

Note: These tests verify the library handles complex schemas without crashes,
not strict performance benchmarks.

Created to ensure the library scales reasonably.
"""

import unittest

from jsonsubschema import isSubschema


class TestLargeSchemas(unittest.TestCase):
    """Test handling of large schemas."""

    def test_many_properties(self):
        """Test object with many properties."""
        props1 = {f"prop{i}": {"type": "string"} for i in range(50)}
        props2 = {f"prop{i}": {"type": "string"} for i in range(100)}

        s1 = {"type": "object", "properties": props1}
        s2 = {"type": "object", "properties": props2}

        result = isSubschema(s1, s2)
        self.assertIsInstance(result, bool)

    def test_many_required_fields(self):
        """Test object with many required fields."""
        props = {f"field{i}": {"type": "integer"} for i in range(30)}
        required1 = [f"field{i}" for i in range(20)]
        required2 = [f"field{i}" for i in range(10)]

        s1 = {"type": "object", "properties": props, "required": required1}
        s2 = {"type": "object", "properties": props, "required": required2}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_large_enum(self):
        """Test enum with many values."""
        enum1 = list(range(100))
        enum2 = list(range(200))

        s1 = {"type": "integer", "enum": enum1}
        s2 = {"type": "integer", "enum": enum2}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_large_allOf(self):
        """Test allOf with many schemas."""
        schemas = [{"type": "integer", "minimum": i, "maximum": 100} for i in range(10)]
        s1 = {"allOf": schemas}
        s2 = {"type": "integer"}

        result = isSubschema(s1, s2)
        self.assertIsInstance(result, bool)

    def test_large_anyOf(self):
        """Test anyOf with many schemas."""
        schemas = [{"type": "integer", "enum": [i]} for i in range(20)]
        s1 = {"anyOf": schemas}
        s2 = {"type": "integer"}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestDeepNesting(unittest.TestCase):
    """Test deeply nested schemas."""

    def test_deeply_nested_objects(self):
        """Test deeply nested object schemas."""
        s1 = {"type": "object"}
        s2 = {"type": "object"}

        for _ in range(10):
            s1 = {"type": "object", "properties": {"nested": s1}}
            s2 = {"type": "object", "properties": {"nested": s2}}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_deeply_nested_arrays(self):
        """Test deeply nested array schemas."""
        s1 = {"type": "integer"}
        s2 = {"type": "integer"}

        for _ in range(10):
            s1 = {"type": "array", "items": s1}
            s2 = {"type": "array", "items": s2}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_deeply_nested_allOf(self):
        """Test deeply nested allOf."""
        s = {"type": "integer"}
        for _ in range(10):
            s = {"allOf": [s]}

        result = isSubschema(s, {"type": "integer"})
        self.assertTrue(result)

    def test_deeply_nested_anyOf(self):
        """Test deeply nested anyOf."""
        s = {"type": "integer"}
        for _ in range(10):
            s = {"anyOf": [s]}

        result = isSubschema(s, {"type": "integer"})
        self.assertTrue(result)


class TestComplexCombinations(unittest.TestCase):
    """Test complex schema combinations."""

    def test_mixed_deep_and_wide(self):
        """Test schema that is both deep and wide."""
        base_props = {
            "prop1": {"type": "string", "minLength": 1},
            "prop2": {"type": "integer", "minimum": 0},
            "prop3": {"type": "boolean"},
        }

        s1 = {
            "type": "object",
            "properties": base_props,
            "required": ["prop1", "prop2"],
        }

        nested_obj = {"type": "object", "properties": {"inner": s1}}
        s2 = {
            "type": "object",
            "properties": {**base_props, "nested": nested_obj},
        }

        result = isSubschema(s1, s2)
        self.assertIsInstance(result, bool)

    def test_multiple_allOf_anyOf_layers(self):
        """Test multiple layers of allOf and anyOf."""
        s1 = {
            "allOf": [
                {"type": "integer"},
                {"anyOf": [{"minimum": 0}, {"maximum": 100}]},
                {"allOf": [{"multipleOf": 2}]},
            ]
        }
        s2 = {"type": "integer"}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_oneOf_with_many_branches(self):
        """Test oneOf with many branches."""
        branches = [
            {"type": "integer", "minimum": i * 10, "maximum": (i + 1) * 10}
            for i in range(10)
        ]
        s1 = {"oneOf": branches}
        s2 = {"type": "integer"}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestLargeConstraintRanges(unittest.TestCase):
    """Test schemas with large constraint values."""

    def test_large_number_range(self):
        """Test number with large range."""
        s1 = {"type": "integer", "minimum": 0, "maximum": 1000000}
        s2 = {"type": "integer", "minimum": -1000000, "maximum": 2000000}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_large_string_length(self):
        """Test string with large length constraints."""
        s1 = {"type": "string", "minLength": 100, "maxLength": 1000}
        s2 = {"type": "string", "minLength": 0, "maxLength": 10000}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_large_array_size(self):
        """Test array with large size constraints."""
        s1 = {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 50,
            "maxItems": 100,
        }
        s2 = {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 0,
            "maxItems": 200,
        }

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_large_multipleOf(self):
        """Test number with large multipleOf."""
        s1 = {"type": "integer", "multipleOf": 1000}
        s2 = {"type": "integer", "multipleOf": 500}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


if __name__ == "__main__":
    unittest.main()
