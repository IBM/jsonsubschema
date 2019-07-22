'''
Created on July 11, 2019
@author: Andrew Habib
'''

import unittest
import warnings

from jsonschema.exceptions import SchemaError

from checker import isSubschema


class TestStringSubtype(unittest.TestCase):

    def test_min_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "string", "minLength": 5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maxLength": 1}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
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
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))
