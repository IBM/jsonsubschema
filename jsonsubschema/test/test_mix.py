'''
Created on June 3, 2019
@author: Andrew Habib
'''

import unittest

from checker import isSubschema


class TestMixedTypes(unittest.TestCase):

    def test_t_t_2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array"}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_t_t_2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": ["number"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_t_t_3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": ["number"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_t_t_4(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": ["number", "string"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_t_t_5(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": ["string", "array"]}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": ["number", "string"]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    
    def test_str_int(self):
        s1 = {
            "$schema": "http://json-schema.org/draft-04/schema",
            "type": "string", "pattern": "a+",
            "allOf": [{"type": "string", "pattern": "b+"}, {"allOf": [{"type": "string", "maxLength": 10}]}]
            }
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maxLength": 1}
        with self.subTest("LHS is uninhabited"):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest("RHS is uninhabited"):
            self.assertFalse(isSubschema(s2, s1))
