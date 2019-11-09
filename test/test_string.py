'''
Created on July 11, 2019
@author: Andrew Habib
'''

import unittest
import warnings

from jsonschema.exceptions import SchemaError

from jsonsubschema import isSubschema, isEquivalent, set_debug


class TestStringSubtype(unittest.TestCase):

    def test_min_min(self):
        s1 = {"type": "string", "minLength": 5}
        s2 = {"type": "integer", "maxLength": 1}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_empty_pattern(self):
        s1 = {"type": "string", "pattern": ""}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_regx_range1(self):
        s1 = {"type": "string", "maxLength": 5, "pattern": "(ab)*"}
        s2 = {"type": "string", "pattern": "(ab){3}"}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_regx_range2(self):
        s1 = {"type": "string", "maxLength": 5, "pattern": "^(ab)*$"}
        s2 = {"type": "string", "pattern": "^(ab){0,3}$"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestNotStringSubtype(unittest.TestCase):

    def test_str_not_str(self):
        s1 = {"type": "string"}
        s2 = {"not": s1}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_str_not_str_with_range(self):
        s1 = {"type": "string"}
        s2 = {"allOf": [{"type": "string"}, {
            "not": {"type": "string", "minLength": 2}}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_str_not_str_with_range2(self):
        s1 = {"type": "string", "maxLength": 1}
        s2 = {"allOf": [{"type": "string"}, {
            "not": {"type": "string", "minLength": 2}}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_str_not_str_with_range3(self):
        s1 = {"type": "string", "minLength": 1, "maxLength": 5}
        s2 = {"allOf": [{"type": "string"}, {
            "not": {"type": "string", "minLength": 2}}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_str_not_str_with_range4(self):
        s1 = {"type": "string", "minLength": 1, "maxLength": 5}
        s2 = {"allOf": [{"type": "string"}, {
            "not": {"type": "string", "minLength": 2}}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_not_str_not_str1(self):
        s1 = {"not": {"type": "string"}}
        s2 = {"not": {"not": {"not": {"type": "string"}}}}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_not_str_not_str2(self):
        s1 = {"not": {"type": "string"}}
        s2 = {"not": {"not": {"type": "string"}}}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_all_str_not_str1(self):
        s1 = {"allOf": [{"type": "string"}, {
            "not": {"type": "string", "minLength": 2}}]}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_all_str_not_str2(self):
        s1 = {"allOf": [{"type": "string"}, {
            "not": {"type": "string", "minLength": 2}}]}
        s2 = {"type": "string", "maxLength": 1}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_all_str_not_str3(self):
        s1 = {"allOf": [{"type": "string"}, {
            "not": {"type": "string", "minLength": 2, "pattern": "ab"}}]}
        s2 = {"type": "string", "maxLength": 1}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_not_str_and_join_string(self):
        s1 = {"allOf": [{"type": "string"}, {
            "not": {"type": "string", "minLength": 5, "pattern": "a"}}]}
        s2 = {"anyOf": [{"type": "string", "maxLength": 4},
                        {"type": "string", "pattern": "[^a]"}]}
        set_debug(True)
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))
        set_debug(False)

    def test_equiv_multiple_case(self):
        s1 = {"type": ["string", "null"], "minLength": 1}
        s2 = {"anyOf": [{"type": "string", "minLength": 1}, {"type": "null"}]}
        s3 = {"anyOf": [{"type": "string", "pattern": ".+"}, {"enum": [None]}]}
        s4 = {"type": ["string", "null"], "pattern": ".{1,}"}
        s5 = {"type": ["string", "null"], "not": {"enum": [""]}}

        with self.subTest():
            self.assertTrue(isEquivalent(s1, s2))
        with self.subTest():
            self.assertTrue(isEquivalent(s1, s3))
        with self.subTest():
            self.assertTrue(isEquivalent(s1, s4))
        with self.subTest():
            self.assertTrue(isEquivalent(s1, s5))
        with self.subTest():
            self.assertTrue(isEquivalent(s2, s3))
        with self.subTest():
            self.assertTrue(isEquivalent(s2, s4))
        with self.subTest():
            self.assertTrue(isEquivalent(s2, s5))
        with self.subTest():
            self.assertTrue(isEquivalent(s3, s4))
        with self.subTest():
            self.assertTrue(isEquivalent(s3, s5))
        with self.subTest():
            self.assertTrue(isEquivalent(s4, s5))

        s6 = {"type": ["string", "null"], "pattern": ".{2,}"}
        s7 = {"type": ["string", "null"], "minLength": 2}

        with self.subTest():
            self.assertTrue(isEquivalent(s6, s7))
        with self.subTest():
            self.assertTrue(isSubschema(s6, s1))
        with self.subTest():
            self.assertFalse(isSubschema(s1, s7))


class TestStringEnumSubtype(unittest.TestCase):

    def test_enum1(self):
        s1 = {"type": "string", "enum": ["a"]}
        s2 = {"enum": ["a"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_enum2(self):
        s1 = {"type": "string", "enum": ["a"]}
        s2 = {"enum": ["a", "b"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_enum3(self):
        s1 = {"type": "string", "enum": ["a", ""]}
        s2 = {"enum": ["a", "b"]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_not_enum1(self):
        s1 = {"type": "string", "not": {"enum": ["a"]}}
        s2 = {"type": "string"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_not_enum2(self):
        s1 = {"type": "string", "not": {"enum": ["a", "b"]}}
        s2 = {"type": "string", "enum": ["a", "b"]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))
