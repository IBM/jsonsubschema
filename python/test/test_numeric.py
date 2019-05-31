'''
Created on May 30, 2019
@author: Andrew Habib
'''

import unittest
import warnings

from subschemachecker import Checker


class TestNumericSubtype(unittest.TestCase):


    def test_identity_number(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
            "type": "number"}
        s2 = s1
        # self.assertWarns(Warning, Checker(s1, s2).is_subschema)
        self.assertTrue(Checker(s1, s2).is_subschema())

    def test_identity_integer(self):
      s1 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "integer"}
      s2 = s1
      self.assertTrue(Checker(s1, s2).is_subschema())

    def test_int_num(self):
      s1 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "integer"}
      s2 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "number"}
      self.assertTrue(Checker(s1, s2).is_subschema())
      self.assertFalse(Checker(s2, s1).is_subschema())

    def test_min_num_num(self):
      s1 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "number", "minimum": 1.5}
      s2 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "number", "minimum": 1}
      self.assertTrue(Checker(s1, s2).is_subschema())
      self.assertFalse(Checker(s2, s1).is_subschema())

    def test_min_num_int(self):
      s1 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "number", "minimum": 1.5}
      s2 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "integer", "minimum": 1}
      self.assertFalse(Checker(s1, s2).is_subschema())
      self.assertFalse(Checker(s2, s1).is_subschema())

    def test_max_int_int(self):
      s1 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "integer", "maximum": 10}
      s2 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "integer", "maximum": 5}
      self.assertFalse(Checker(s1, s2).is_subschema())
      self.assertTrue(Checker(s2, s1).is_subschema())

    def test_max_int_min_int(self):
      s1 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "integer", "maximum": 10}
      s2 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "integer", "minimum": 5}
      self.assertFalse(Checker(s1, s2).is_subschema())
      self.assertFalse(Checker(s2, s1).is_subschema())

    def test_mulfof_num_min_int(self):
      s1 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "number", "multipleOf": 10}
      s2 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "integer", "minimum": 5}
      self.assertFalse(Checker(s1, s2).is_subschema())
      self.assertFalse(Checker(s2, s1).is_subschema())

    def test_mulfof_num_int(self):
      s1 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "number", "multipleOf": 10}
      s2 = {"$schema": "http://json-schema.org/draft-04/schema",
          "type": "integer"}
      self.assertTrue(Checker(s1, s2).is_subschema())
      self.assertFalse(Checker(s2, s1).is_subschema())

if __name__ == "__main__":
    unittest.main()
