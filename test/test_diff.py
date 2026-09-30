"""Tests for schemaDiff API."""

import unittest

from jsonsubschema import schemaDiff


class TestSchemaDiff(unittest.TestCase):

    def test_equivalent(self):
        s1 = {"type": "string"}
        s2 = {"type": "string"}
        self.assertEqual(schemaDiff(s1, s2), "equivalent")

    def test_equivalent_reordered_type_list(self):
        s1 = {"type": ["string", "null"]}
        s2 = {"type": ["null", "string"]}
        self.assertEqual(schemaDiff(s1, s2), "equivalent")

    def test_backward_compatible(self):
        """s1 is more restrictive than s2 (s1 <: s2)."""
        s1 = {"type": "integer", "minimum": 0, "maximum": 10}
        s2 = {"type": "integer"}
        self.assertEqual(schemaDiff(s1, s2), "backward_compatible")

    def test_forward_compatible(self):
        """s2 is more restrictive than s1 (s2 <: s1)."""
        s1 = {"type": "integer"}
        s2 = {"type": "integer", "minimum": 0, "maximum": 10}
        self.assertEqual(schemaDiff(s1, s2), "forward_compatible")

    def test_breaking(self):
        """Neither direction holds."""
        s1 = {"type": "string"}
        s2 = {"type": "integer"}
        self.assertEqual(schemaDiff(s1, s2), "breaking")

    def test_washington_post_example(self):
        """Example from the paper: API schema evolution."""
        v061 = {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["staff", "wires", "other"]
                }
            }
        }
        v062 = {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["staff", "wires", "stock", "other"]
                }
            }
        }
        # v0.6.1 <: v0.6.2 (old is subtype of new — backward compatible)
        # v0.6.2 is NOT <: v0.6.1 (new has "stock" which old doesn't accept)
        self.assertEqual(schemaDiff(v061, v062), "backward_compatible")

    def test_enum_subset(self):
        s1 = {"enum": [1, 2]}
        s2 = {"enum": [1, 2, 3]}
        self.assertEqual(schemaDiff(s1, s2), "backward_compatible")

    def test_enum_equal(self):
        s1 = {"enum": [1, 2]}
        s2 = {"enum": [2, 1]}
        self.assertEqual(schemaDiff(s1, s2), "equivalent")
