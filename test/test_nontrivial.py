"""
Test suite for nontrivial JSON subschema relationships.

This module tests complex real-world scenarios including:
- Realistic schema evolution scenarios
- Complex nested structures
- Multiple constraint interactions
- Practical API versioning cases

Created to ensure the library handles real-world schema relationships correctly.
"""

import unittest

from jsonsubschema import isSubschema


class TestSchemaEvolution(unittest.TestCase):
    """Test realistic schema evolution scenarios."""

    def test_api_backward_compatible_addition(self):
        """Test adding optional field maintains backward compatibility."""
        old_version = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        }
        new_version = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
            },
            "required": ["name"],
        }
        with self.subTest():
            self.assertFalse(isSubschema(old_version, new_version))
        with self.subTest():
            self.assertTrue(isSubschema(new_version, old_version))

    def test_api_breaking_change_required_field(self):
        """Test adding required field breaks backward compatibility."""
        old_version = {
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": ["name"],
        }
        new_version = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
            },
            "required": ["name", "email"],
        }
        with self.subTest():
            self.assertFalse(isSubschema(old_version, new_version))
        with self.subTest():
            self.assertTrue(isSubschema(new_version, old_version))

    def test_api_relaxing_constraint(self):
        """Test relaxing constraint is backward compatible."""
        strict_schema = {
            "type": "object",
            "properties": {"age": {"type": "integer", "minimum": 0, "maximum": 120}},
        }
        relaxed_schema = {
            "type": "object",
            "properties": {"age": {"type": "integer", "minimum": 0}},
        }
        with self.subTest():
            self.assertTrue(isSubschema(strict_schema, relaxed_schema))
        with self.subTest():
            self.assertFalse(isSubschema(relaxed_schema, strict_schema))

    def test_api_narrowing_type_union(self):
        """Test narrowing type union breaks backward compatibility."""
        wide_union = {
            "type": "object",
            "properties": {"value": {"type": ["string", "integer", "null"]}},
        }
        narrow_union = {
            "type": "object",
            "properties": {"value": {"type": ["string", "integer"]}},
        }
        with self.subTest():
            self.assertTrue(isSubschema(narrow_union, wide_union))
        with self.subTest():
            self.assertFalse(isSubschema(wide_union, narrow_union))


class TestNestedStructures(unittest.TestCase):
    """Test complex nested schema structures."""

    def test_deeply_nested_objects(self):
        """Test deeply nested object structures."""
        s1 = {
            "type": "object",
            "properties": {
                "level1": {
                    "type": "object",
                    "properties": {
                        "level2": {
                            "type": "object",
                            "properties": {
                                "level3": {
                                    "type": "object",
                                    "properties": {"value": {"type": "integer"}},
                                    "required": ["value"],
                                }
                            },
                            "required": ["level3"],
                        }
                    },
                    "required": ["level2"],
                }
            },
            "required": ["level1"],
        }
        s2 = {
            "type": "object",
            "properties": {
                "level1": {
                    "type": "object",
                    "properties": {
                        "level2": {
                            "type": "object",
                            "properties": {
                                "level3": {"type": "object", "properties": {}}
                            },
                        }
                    },
                }
            },
        }
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_array_of_complex_objects(self):
        """Test array containing complex object schemas."""
        s1 = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string", "minLength": 1},
                    "tags": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["id", "name"],
            },
            "minItems": 1,
        }
        s2 = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                },
            },
        }
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mixed_allOf_anyOf_combination(self):
        """Test complex combination of allOf and anyOf."""
        s1 = {
            "allOf": [
                {"type": "integer", "minimum": 10, "maximum": 50},
                {"anyOf": [{"maximum": 20}, {"minimum": 40}]},
            ]
        }
        s2 = {"type": "integer", "minimum": 10, "maximum": 50}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestMultiConstraintInteraction(unittest.TestCase):
    """Test interactions between multiple constraints."""

    def test_string_all_constraints(self):
        """Test string with multiple constraints combined."""
        s1 = {
            "type": "string",
            "minLength": 5,
            "maxLength": 10,
        }
        s2 = {"type": "string", "minLength": 3, "maxLength": 15}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_number_multiple_of_with_range(self):
        """Test number with multipleOf and range constraints."""
        s1 = {
            "type": "integer",
            "minimum": 10,
            "maximum": 100,
            "multipleOf": 5,
        }
        s2 = {"type": "integer", "minimum": 0, "maximum": 200}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_array_all_constraints(self):
        """Test array with multiple constraints combined."""
        s1 = {
            "type": "array",
            "items": {"type": "integer", "minimum": 0},
            "minItems": 2,
            "maxItems": 5,
            "uniqueItems": True,
        }
        s2 = {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 1,
            "maxItems": 10,
        }
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_object_all_constraints(self):
        """Test object with multiple constraints combined."""
        s1 = {
            "type": "object",
            "properties": {
                "a": {"type": "string"},
                "b": {"type": "integer"},
            },
            "required": ["a", "b"],
            "minProperties": 2,
            "maxProperties": 3,
            "additionalProperties": {"type": "boolean"},
        }
        s2 = {
            "type": "object",
            "properties": {
                "a": {"type": "string"},
                "b": {"type": "integer"},
            },
            "required": ["a"],
        }
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestRealWorldPatterns(unittest.TestCase):
    """Test patterns from real-world JSON schemas."""

    def test_json_rpc_request(self):
        """Test JSON-RPC 2.0 request schema evolution."""
        basic_request = {
            "type": "object",
            "properties": {
                "jsonrpc": {"type": "string", "enum": ["2.0"]},
                "method": {"type": "string"},
                "id": {"type": ["string", "integer", "null"]},
            },
            "required": ["jsonrpc", "method", "id"],
        }
        extended_request = {
            "type": "object",
            "properties": {
                "jsonrpc": {"type": "string", "enum": ["2.0"]},
                "method": {"type": "string"},
                "params": {
                    "anyOf": [
                        {"type": "array"},
                        {"type": "object"},
                    ]
                },
                "id": {"type": ["string", "integer", "null"]},
            },
            "required": ["jsonrpc", "method", "id"],
        }
        with self.subTest():
            self.assertFalse(isSubschema(basic_request, extended_request))
        with self.subTest():
            self.assertTrue(isSubschema(extended_request, basic_request))

    def test_geojson_point(self):
        """Test GeoJSON Point schema."""
        strict_point = {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["Point"]},
                "coordinates": {
                    "type": "array",
                    "items": {"type": "number"},
                    "minItems": 2,
                    "maxItems": 3,
                },
            },
            "required": ["type", "coordinates"],
        }
        relaxed_point = {
            "type": "object",
            "properties": {
                "type": {"type": "string"},
                "coordinates": {"type": "array", "items": {"type": "number"}},
            },
            "required": ["type", "coordinates"],
        }
        with self.subTest():
            self.assertTrue(isSubschema(strict_point, relaxed_point))
        with self.subTest():
            self.assertFalse(isSubschema(relaxed_point, strict_point))

    def test_package_json_dependencies(self):
        """Test package.json dependencies schema."""
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
                "dependencies": {
                    "type": "object",
                    "patternProperties": {".*": {"type": "string"}},
                    "additionalProperties": False,
                },
            },
            "required": ["name", "version"],
        }
        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "version": {"type": "string"},
            },
            "required": ["name", "version"],
        }
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


if __name__ == "__main__":
    unittest.main()
