'''
Created on May 30, 2019
@author: Andrew Habib
'''

import unittest

from jsonsubschema.checker import isSubschema


class TestArraySubtype(unittest.TestCase):

    def test_identity(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array",
              "minItems": 5, "maxItems:": 10}
        s2 = s1
        self.assertTrue(isSubschema(s1, s2))

    def test_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array",
              "minItems": 5, "maxItems:": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array",
              "minItems": 1, "maxItems:": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_unique(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "uniqueItems": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "uniqueItems": False}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_empty_items1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": {}}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_empty_items2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "additionalItems": False}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": {}}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_empty_items3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{}, {}], "additionalItems": False}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": {}}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_empty_items4(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{}, {}], "additionalItems": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": {}}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_empty_items5(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{}, {}], "additionalItems": False}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{}], "additionalItems": False}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_dictItems_listItems1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": {"type": "string"}}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{"type": "string"}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_dictItems_listItems2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": {"type": "string"}}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{"type": "string"}, {"type": "string"}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_dictItems_listItems3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{"type": "string"}]}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{"type": "string"}, {"type": "number"}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_dictItems_listItems4(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{"type": "string"}], "additionalItems": False}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{"type": "string"}, {"type": "number"}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_dictItems_listItems5(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{"type": "string"}], "additionalItems": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{"type": "string"}, {"type": "number"}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_dictItems_listItems6(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{"type": "string"}], "additionalItems": {}}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "items": [{"type": "string"}, {"type": "number"}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))
