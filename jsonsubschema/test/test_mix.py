'''
Created on June 3, 2019
@author: Andrew Habib
'''

import unittest

from subschemachecker import Checker

class TestMixedTypes(unittest.TestCase):

    def test_t_t_2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array"}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_t_t_2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": ["number"]}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertTrue(Checker(s2, s1).is_subschema())

    def test_t_t_3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": ["number"]}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_t_t_4(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": ["number", "string"]}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_t_t_5(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": ["string", "array"]}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": ["number", "string"]}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())
