"""
Created on Jan 18, 2026
Test coverage for all exception classes in jsonsubschema.exceptions

This test suite ensures that all custom exceptions are properly raised
under the appropriate conditions:
- UnsupportedRecursiveRef: Recursive $ref handling
- UnsupportedNegatedArray: Negation of arrays with constraints
- UnsupportedNegatedObject: Negation of objects with constraints
- UnsupportedEnumCanonicalization: Enum canonicalization for certain types
"""

import unittest

from jsonsubschema import isSubschema
from jsonsubschema.exceptions import (
    UnsupportedRecursiveRef,
    UnsupportedNegatedArray,
    UnsupportedNegatedObject,
    UnsupportedEnumCanonicalization,
)


class TestUnsupportedRecursiveRef(unittest.TestCase):
    """Test cases for UnsupportedRecursiveRef exception"""

    def test_recursive_ref_in_rhs(self):
        """Recursive $ref in RHS triggers recursion detection during canonicalization"""
        s1 = {"enum": [None]}
        s2 = {
            "definitions": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "children": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/person"},
                            "default": [],
                        },
                    },
                }
            },
            "type": "object",
            "properties": {"person": {"$ref": "#/definitions/person"}},
        }

        with self.assertRaises(UnsupportedRecursiveRef) as cm:
            isSubschema(s1, s2)

        self.assertIn("Recursive schemas are not supported", str(cm.exception))
        self.assertEqual(cm.exception.which_side, "RHS")


class TestUnsupportedNegatedArray(unittest.TestCase):
    """Test cases for UnsupportedNegatedArray exception"""

    def test_negation_of_array_with_items(self):
        """Negating an array schema with items constraint should raise exception"""
        s1 = {"type": "string"}
        s2 = {"not": {"type": "array", "items": {"type": "string"}}}

        with self.assertRaises(UnsupportedNegatedArray) as cm:
            isSubschema(s1, s2)

        self.assertIn("Array negation", str(cm.exception))

    def test_negation_of_array_with_minitems_now_supported(self):
        """Negating an array schema with minItems is now supported"""
        s1 = {"type": "integer"}
        s2 = {"not": {"type": "array", "minItems": 1}}
        # integer is not an array, so always subtype of not(array)
        self.assertTrue(isSubschema(s1, s2))

    def test_negation_of_array_with_maxitems_now_supported(self):
        """Negating an array schema with maxItems is now supported"""
        s1 = {"type": "boolean"}
        s2 = {"not": {"type": "array", "maxItems": 5}}
        # boolean is not an array, so always subtype of not(array)
        self.assertTrue(isSubschema(s1, s2))

    def test_negation_of_array_with_uniqueitems(self):
        """Negating an array schema with uniqueItems should raise exception"""
        s1 = {"type": "null"}
        s2 = {"not": {"type": "array", "uniqueItems": True}}

        with self.assertRaises(UnsupportedNegatedArray) as cm:
            isSubschema(s1, s2)

    def test_negation_of_plain_array_succeeds(self):
        """Negating a plain array without constraints should succeed"""
        s1 = {"type": "string"}
        s2 = {"not": {"type": "array"}}

        result = isSubschema(s1, s2)
        self.assertTrue(result)


class TestUnsupportedNegatedObject(unittest.TestCase):
    """Test cases for UnsupportedNegatedObject exception"""

    def test_negation_of_object_with_properties(self):
        """Negating an object schema with properties should raise exception"""
        s1 = {"type": "string"}
        s2 = {"not": {"type": "object", "properties": {"name": {"type": "string"}}}}

        with self.assertRaises(UnsupportedNegatedObject) as cm:
            isSubschema(s1, s2)

        self.assertIn("Object negation", str(cm.exception))

    def test_negation_of_object_with_required(self):
        """Negating an object schema with required should raise exception"""
        s1 = {"type": "integer"}
        s2 = {"not": {"type": "object", "required": ["id"]}}

        with self.assertRaises(UnsupportedNegatedObject) as cm:
            isSubschema(s1, s2)

    def test_negation_of_object_with_additionalproperties(self):
        """Negating an object schema with additionalProperties should raise exception"""
        s1 = {"type": "boolean"}
        s2 = {"not": {"type": "object", "additionalProperties": False}}

        with self.assertRaises(UnsupportedNegatedObject) as cm:
            isSubschema(s1, s2)

    def test_negation_of_object_with_minproperties_now_supported(self):
        """Negating an object schema with minProperties is now supported"""
        s1 = {"type": "null"}
        s2 = {"not": {"type": "object", "minProperties": 1}}
        # null is not an object, so always subtype of not(object)
        self.assertTrue(isSubschema(s1, s2))

    def test_negation_of_object_with_maxproperties_now_supported(self):
        """Negating an object schema with maxProperties is now supported"""
        s1 = {"type": "array"}
        s2 = {"not": {"type": "object", "maxProperties": 10}}
        # array is not an object, so always subtype of not(object)
        self.assertTrue(isSubschema(s1, s2))

    def test_negation_of_plain_object_succeeds(self):
        """Negating a plain object without constraints should succeed"""
        s1 = {"type": "string"}
        s2 = {"not": {"type": "object"}}

        result = isSubschema(s1, s2)
        self.assertTrue(result)


class TestUnsupportedEnumCanonicalization(unittest.TestCase):
    """Test cases for UnsupportedEnumCanonicalization exception"""

    def test_array_enum_canonicalization_now_supported(self):
        """Enum with array type is now supported via pushdown"""
        s1 = {"type": "array", "enum": [[1, 2], [3, 4, 5]]}
        s2 = {"type": "array"}

        result = isSubschema(s1, s2)
        self.assertTrue(result)

    def test_object_enum_canonicalization_now_supported(self):
        """Enum with object type is now supported via pushdown"""
        s1 = {"type": "object", "enum": [{"name": "Alice"}, {"name": "Bob", "age": 30}]}
        s2 = {"type": "object"}

        result = isSubschema(s1, s2)
        self.assertTrue(result)

    def test_integer_enum_succeeds(self):
        """Enum with integer type should succeed (supported)"""
        s1 = {"type": "integer", "enum": [1, 2, 3]}
        s2 = {"type": "integer"}

        result = isSubschema(s1, s2)
        self.assertTrue(result)

    def test_string_enum_succeeds(self):
        """Enum with string type should succeed (supported)"""
        s1 = {"type": "string", "enum": ["foo", "bar"]}
        s2 = {"type": "string"}

        result = isSubschema(s1, s2)
        self.assertTrue(result)

    def test_boolean_enum_succeeds(self):
        """Enum with boolean type should succeed (supported)"""
        s1 = {"type": "boolean", "enum": [True, False]}
        s2 = {"type": "boolean"}

        result = isSubschema(s1, s2)
        self.assertTrue(result)

    def test_null_enum_succeeds(self):
        """Enum with null type should succeed (supported)"""
        s1 = {"type": "null", "enum": [None]}
        s2 = {"type": "null"}

        result = isSubschema(s1, s2)
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
