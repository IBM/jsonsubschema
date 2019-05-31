'''
Created on May 30, 2019
@author: Andrew Habib
'''

import unittest

from subschemachecker import Checker


class TestArraySubtype(unittest.TestCase):

    def test_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array",
              "minItems": 5, "maxItems:": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array",
              "minItems": 1, "maxItems:": 20}
        self.assertTrue(Checker(s1, s2).is_subschema())
        self.assertFalse(Checker(s2, s1).is_subschema())

    def test_unique(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "uniqueItems": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "array", "uniqueItems": False}
        self.assertTrue(Checker(s1, s2).is_subschema())
        self.assertFalse(Checker(s2, s1).is_subschema())
