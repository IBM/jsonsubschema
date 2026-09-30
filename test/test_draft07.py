"""Tests for Draft-07 features: if/then/else and contains."""

import unittest

from jsonsubschema import isSubschema


class TestIfThenElse(unittest.TestCase):
    """Tests for if/then/else canonicalization."""

    def test_if_then_else_basic(self):
        """if type is string, then minLength 1; else must be integer."""
        s1 = {
            "if": {"type": "string"},
            "then": {"minLength": 1},
            "else": {"type": "integer"}
        }
        # A non-empty string satisfies: if=string matches, then minLength 1
        s2 = {"type": "string", "minLength": 1}
        self.assertTrue(isSubschema(s2, s1))

    def test_if_then_else_integer_branch(self):
        """Integer should satisfy the else branch."""
        s1 = {
            "if": {"type": "string"},
            "then": {"minLength": 1},
            "else": {"type": "integer"}
        }
        s2 = {"type": "integer"}
        self.assertTrue(isSubschema(s2, s1))

    def test_if_then_else_reject_empty_string(self):
        """Empty string should NOT satisfy (if matches string, then requires minLength 1)."""
        s1 = {
            "if": {"type": "string"},
            "then": {"minLength": 1},
            "else": {"type": "integer"}
        }
        s2 = {"type": "string"}  # includes empty string
        self.assertFalse(isSubschema(s2, s1))

    def test_if_then_no_else(self):
        """if/then without else: else defaults to {} (accept everything)."""
        s1 = {
            "if": {"type": "string"},
            "then": {"minLength": 1}
        }
        # Integers match the else branch ({} accepts everything)
        s2 = {"type": "integer"}
        self.assertTrue(isSubschema(s2, s1))

    def test_if_then_else_with_type(self):
        """if/then/else combined with type constraint."""
        s1 = {
            "type": "integer",
            "if": {"minimum": 0},
            "then": {"maximum": 100},
            "else": {"minimum": -100}
        }
        # integers in [0, 100] satisfy: if >=0 matches, then <=100
        s2 = {"type": "integer", "minimum": 0, "maximum": 100}
        self.assertTrue(isSubschema(s2, s1))


class TestContains(unittest.TestCase):
    """Tests for array contains keyword."""

    def test_contains_basic(self):
        """Array with all-string items satisfies contains: string."""
        s1 = {"type": "array", "items": {"type": "string"}}
        s2 = {"type": "array", "contains": {"type": "string"}}
        self.assertTrue(isSubschema(s1, s2))

    def test_contains_subtype(self):
        """contains with subtype relationship."""
        s1 = {"type": "array", "contains": {"type": "integer"}}
        s2 = {"type": "array", "contains": {"type": "number"}}
        # integer <: number, so contains integer <: contains number
        self.assertTrue(isSubschema(s1, s2))

    def test_contains_not_subtype(self):
        """contains that doesn't satisfy."""
        s1 = {"type": "array", "contains": {"type": "string"}}
        s2 = {"type": "array", "contains": {"type": "integer"}}
        self.assertFalse(isSubschema(s1, s2))

    def test_contains_with_items(self):
        """Array with tuple items where one matches contains."""
        s1 = {
            "type": "array",
            "items": [{"type": "integer"}, {"type": "string"}],
            "additionalItems": False
        }
        s2 = {"type": "array", "contains": {"type": "integer"}}
        # First item is integer, so contains integer is satisfied
        self.assertTrue(isSubschema(s1, s2))
