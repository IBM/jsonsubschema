'''
Created on May 30, 2019
@author: Andrew Habib
'''

import unittest
import warnings

from subschemachecker import Checker


class TestIntegerSubtype(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("************************")
        print("Testing integer subtypes")
        print("************************")

    def test_identity(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        s2 = s1
        self.assertTrue(Checker(s1, s2).is_subschema())

    def test_min_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 1}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_max_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maximum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maximum": 5}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertTrue(Checker(s2, s1).is_subschema())

    def test_max_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maximum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maximum": 20}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_min_max_min_max1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 1, "maximum": 20}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_min_max_min_max2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 10, "maximum": 20}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertTrue(Checker(s2, s1).is_subschema())

    def test_min_max_min_max3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 40, "maximum": 100}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_xmin_max_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 20}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_xmin_max_min_xmax(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 20, "exclusiveMaximum": True}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_xmin_xmax_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 20}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_min_max_xmin_xmax1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 6, "maximum": 19}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertTrue(Checker(s2, s1).is_subschema())

    def test_min_max_xmin_xmax2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 6, "maximum": 20}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_xmin_xmax_xmin_xmax(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": False, "maximum": 20, "exclusiveMaximum": True}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 20, "exclusiveMaximum": True}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertTrue(Checker(s2, s1).is_subschema())

    def test_mulfof1(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_mulfof2(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 5}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_mulfof3(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 98}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_mulfof_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_mulfof_min_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10, "minimum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5}
        with self.subTest():
            self.assertTrue(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())

    def test_mulfof_min_min_max(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "multipleOf": 10, "minimum": 10}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 5, "maximum": 500}
        with self.subTest():
            self.assertFalse(Checker(s1, s2).is_subschema())
        with self.subTest():
            self.assertFalse(Checker(s2, s1).is_subschema())


class TestNumberSubtype(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("************************")
        print("Testing number subtypes")
        print("************************")

    def test_identity_number(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number"}
        s2 = s1
        self.assertTrue(Checker(s1, s2).is_subschema())

    def test_min_num_num(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 1.5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 1}
        self.assertTrue(Checker(s1, s2).is_subschema())
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


class TestNumericSubtype(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("************************")
        print("Testing numeric subtypes")
        print(" integers <?--?> numbers")
        print("************************")

    def test_int_num(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer"}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number"}
        self.assertTrue(Checker(s1, s2).is_subschema())
        self.assertFalse(Checker(s2, s1).is_subschema())

    def test_min_num_int(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "number", "minimum": 1.5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "minimum": 1}
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
