'''
Created on May 30, 2019
@author: Andrew Habib
'''

import unittest

from jsonschema.exceptions import SchemaError

from jsonsubschema import isSubschema


class TestIntegerSubtype(unittest.TestCase):

    def test_identity(self):
        s1 = {"type": "integer"}
        s2 = s1
        self.assertTrue(isSubschema(s1, s2))

    def test_min_min(self):
        s1 = {"type": "integer", "minimum": 5}
        s2 = {"type": "integer", "minimum": 1}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_max_max(self):
        s1 = {"type": "integer", "maximum": 10}
        s2 = {"type": "integer", "maximum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_max_min(self):
        s1 = {"type": "integer", "maximum": 10}
        s2 = {"type": "integer", "minimum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max(self):
        s1 = {"type": "integer", "minimum": 10}
        s2 = {"type": "integer", "maximum": 20}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_min_max1(self):
        s1 = {"type": "integer", "minimum": 5, "maximum": 10}
        s2 = {"type": "integer", "minimum": 1, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_min_max2(self):
        s1 = {"type": "integer", "minimum": 5, "maximum": 20}
        s2 = {"type": "integer", "minimum": 10, "maximum": 20}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_min_max_min_max3(self):
        s1 = {"type": "integer", "minimum": 5, "maximum": 20}
        s2 = {"type": "integer", "minimum": 40, "maximum": 100}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_max_min_max(self):
        s1 = {"type": "integer", "minimum": 5,
              "exclusiveMinimum": True, "maximum": 20}
        s2 = {"type": "integer", "minimum": 5, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_max_min_xmax(self):
        s1 = {"type": "integer", "minimum": 5,
              "exclusiveMinimum": True, "maximum": 20}
        s2 = {"type": "integer", "minimum": 5,
              "maximum": 20, "exclusiveMaximum": True}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_xmax_min_max(self):
        s1 = {"type": "integer", "minimum": 5, "exclusiveMinimum": True,
              "maximum": 20, "exclusiveMaximum": True}
        s2 = {"type": "integer", "minimum": 5, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_xmin_xmax1(self):
        s1 = {"type": "integer", "minimum": 5, "exclusiveMinimum": True,
              "maximum": 20, "exclusiveMaximum": True}
        s2 = {"type": "integer", "minimum": 6, "maximum": 19}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_min_max_xmin_xmax2(self):
        s1 = {"type": "integer", "minimum": 5, "exclusiveMinimum": True,
              "maximum": 20, "exclusiveMaximum": True}
        s2 = {"type": "integer", "minimum": 6, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_xmax_xmin_xmax(self):
        s1 = {"type": "integer", "minimum": 5, "exclusiveMinimum": False,
              "maximum": 20, "exclusiveMaximum": True}
        s2 = {"type": "integer", "minimum": 5, "exclusiveMinimum": True,
              "maximum": 20, "exclusiveMaximum": True}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_mulOf1(self):
        s1 = {"type": "integer", "multipleOf": 10}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf2(self):
        s1 = {"type": "integer", "multipleOf": 10}
        s2 = {"type": "integer", "multipleOf": 5}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf3(self):
        s1 = {"type": "integer", "multipleOf": 10}
        s2 = {"type": "integer", "multipleOf": 98}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min(self):
        s1 = {"type": "integer", "multipleOf": 10}
        s2 = {"type": "integer", "minimum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min_min(self):
        s1 = {"type": "integer", "multipleOf": 10, "minimum": 10}
        s2 = {"type": "integer", "minimum": 5}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min_min_max(self):
        s1 = {"type": "integer", "multipleOf": 10, "minimum": 10}
        s2 = {"type": "integer", "minimum": 5, "maximum": 500}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_mul(self):
        s1 = {"type": "integer", "minimum": 5, "maximum": 10, "multipleOf": 15}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_join1(self):
        s1 = {"anyOf": [{"type": "integer", "minimum": 5,
                         "maximum": 10}, {"type": "integer", }]}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_join2(self):
        s1 = {"anyOf": [{"type": "integer", "minimum": 5, "maximum": 10},
                        {"type": "integer", "minimum": 0}]}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_join3(self):
        s1 = {"anyOf": [{"type": "integer", "minimum": 5, "maximum": 10},
                        {"type": "integer", "minimum": 0, "maximum": 3}]}
        s2 = {"type": "integer", "minimum": -1}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_join4(self):
        s1 = {"anyOf": [{"type": "integer", "minimum": 5, "maximum": 10},
                        {"type": "integer", "minimum": 0, "maximum": 4}]}
        s2 = {"type": "integer", "minimum": 1, "maximum": 8}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_join5(self):
        s1 = {"anyOf": [{"type": "integer", "minimum": 5, "exclusiveMinimum": True, "maximum": 10},
                        {"type": "integer", "minimum": 0, "maximum": 4}]}
        s2 = {"type": "integer", "minimum": 1, "maximum": 8}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_join6(self):
        s1 = {"anyOf": [{"type": "integer", "minimum": 0, "maximum": 10},
                        {"type": "integer", "minimum": 11}]}
        s2 = {"type": "integer", "minimum": 0}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_join_mulof1(self):
        s1 = {"anyOf": [{"type": "integer", "multipleOf": 5},
                        {"type": "integer"}]}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_join_mulof2(self):
        s1 = {"anyOf": [{"type": "integer", "multipleOf": 5},
                        {"type": "integer", "multipleOf": 7}]}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_join_mulof3(self):
        s1 = {"anyOf": [{"type": "integer", "multipleOf": 5},
                        {"type": "integer", "multipleOf": 7}]}
        s2 = {"type": "integer", "multipleOf": 35}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_join_mulof4(self):
        s1 = {"anyOf": [{"type": "integer", "multipleOf": 5},
                        {"type": "integer", "multipleOf": 7}]}
        s2 = {"type": "integer", "multipleOf": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_join_mulof5(self):
        s1 = {"anyOf": [{"type": "integer", "multipleOf": 3},
                        {"type": "integer", "multipleOf": 6}]}
        s2 = {"type": "integer", "multipleOf": 3}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_join_mulof6(self):
        s1 = {"anyOf": [{"type": "integer", "multipleOf": 12},
                        {"type": "integer", "multipleOf": 9}]}
        s2 = {"type": "integer", "multipleOf": 3}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_join_mulof7(self):
        s1 = {"anyOf": [{"type": "integer", "multipleOf": 3, "maximum": 10},
                        {"type": "integer", "multipleOf": 5}]}
        s2 = {"type": "integer", "multipleOf": 3}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_join_mulof8(self):
        s1 = {"anyOf": [{"type": "integer", "minimum": 5, "maximum": 15, "multipleOf": 5},
                        {"type": "integer", "minimum": 5, "maximum": 15, "multipleOf": 3}]}
        s2 = {"anyOf": [{"type": "integer", "minimum": 0, "maximum": 12, "multipleOf": 3},
                        {"type": "integer", "minimum": 1, "maximum": 20, "multipleOf": 5}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_join_mulof9(self):
        s1 = {"type": "integer", "minimum": -4, "maximum": 10, "multipleOf": 5}
        s2 = {"anyOf": [{"type": "integer", "minimum": 0, "maximum": 20, "multipleOf": 10},
                        {"type": "integer", "minimum": 1, "maximum": 10, "multipleOf": 5}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    # @unittest.skip("Corner case of multipleOf") # check canonicalization/rewrite_enum
    def test_join_mulof10(self):
        s1 = {"enum": [1, 3, 5, 7, 9, 10]}
        s2 = {"anyOf": [{"type": "integer", "minimum": 0, "maximum": 20, "multipleOf": 10}, {
            "type": "integer", "minimum": 1, "maximum": 10, "multipleOf": 5}, {"enum": [1, 3, 7, 9]}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestNumberSubtype(unittest.TestCase):

    def test_identity(self):
        s1 = {"type": "number"}
        s2 = s1
        self.assertTrue(isSubschema(s1, s2))

    def test_min_min(self):
        s1 = {"type": "number", "minimum": 5}
        s2 = {"type": "number", "minimum": 1}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_max_max(self):
        s1 = {"type": "number", "maximum": 10}
        s2 = {"type": "number", "maximum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_max_min(self):
        s1 = {"type": "number", "maximum": 10}
        s2 = {"type": "number", "minimum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max(self):
        s1 = {"type": "number", "minimum": 10}
        s2 = {"type": "number", "maximum": 20}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_min_max1(self):
        s1 = {"type": "number", "minimum": 5, "maximum": 10}
        s2 = {"type": "number", "minimum": 1, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_min_max2(self):
        s1 = {"type": "number", "minimum": 5, "maximum": 20}
        s2 = {"type": "number", "minimum": 10, "maximum": 20}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_min_max_min_max3(self):
        s1 = {"type": "number", "minimum": 5, "maximum": 20}
        s2 = {"type": "number", "minimum": 40, "maximum": 100}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_max_min_max(self):
        s1 = {"type": "number", "minimum": 5,
              "exclusiveMinimum": True, "maximum": 20}
        s2 = {"type": "number", "minimum": 5, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_max_min_xmax(self):
        s1 = {"type": "number", "minimum": 5,
              "exclusiveMinimum": True, "maximum": 20}
        s2 = {"type": "number", "minimum": 5,
              "maximum": 20, "exclusiveMaximum": True}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_xmax_min_max(self):
        s1 = {"type": "number", "minimum": 5, "exclusiveMinimum": True,
              "maximum": 20, "exclusiveMaximum": True}
        s2 = {"type": "number", "minimum": 5, "maximum": 20}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_xmin_xmax1(self):
        s1 = {"type": "number", "minimum": 5, "exclusiveMinimum": True,
              "maximum": 20, "exclusiveMaximum": True}
        s2 = {"type": "number", "minimum": 6, "maximum": 19}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_min_max_xmin_xmax2(self):
        s1 = {"type": "number", "minimum": 5, "exclusiveMinimum": True,
              "maximum": 20, "exclusiveMaximum": True}
        s2 = {"type": "number", "minimum": 6, "maximum": 20}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_xmin_xmax_xmin_xmax(self):
        s1 = {"type": "number", "minimum": 5, "exclusiveMinimum": False,
              "maximum": 20, "exclusiveMaximum": True}
        s2 = {"type": "number", "minimum": 5, "exclusiveMinimum": True,
              "maximum": 20, "exclusiveMaximum": True}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_mulOf1(self):
        s1 = {"type": "number", "multipleOf": 10.5}
        s2 = {"type": "number"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf2(self):
        s1 = {"type": "number", "multipleOf": 1.5}
        s2 = {"type": "number", "multipleOf": 6}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_mulOf3(self):
        s1 = {"type": "number", "multipleOf": .5}
        s2 = {"type": "number", "multipleOf": -.5}
        self.assertRaises(SchemaError, isSubschema, s1, s2)

    def test_mulOf4(self):
        s1 = {"type": "number", "multipleOf": 1}
        s2 = {"type": "number"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min(self):
        s1 = {"type": "number", "multipleOf": 10}
        s2 = {"type": "number", "minimum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min_min(self):
        s1 = {"type": "number", "multipleOf": 10, "minimum": 10}
        s2 = {"type": "number", "minimum": 5}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_min_min_max(self):
        s1 = {"type": "number", "multipleOf": 10, "minimum": 10}
        s2 = {"type": "number", "minimum": 5, "maximum": 500}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


class TestNumericSubtype(unittest.TestCase):

    def test_int_num(self):
        s1 = {"type": "integer"}
        s2 = {"type": "number"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_num_int(self):
        s1 = {"type": "number", "minimum": 1.5}
        s2 = {"type": "integer", "minimum": 1}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_num_min_int(self):
        s1 = {"type": "number", "multipleOf": 10}
        s2 = {"type": "integer", "minimum": 5}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_num_int(self):
        s1 = {"type": "number", "multipleOf": 10}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_mulOf_num_int2(self):
        s1 = {"type": "number", "multipleOf": 1}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_decimal1(self):
        s1 = {'maximum': 10.}
        s2 = {'maximum': 10}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('RHS > LHS'):
            self.assertTrue(isSubschema(s2, s1))

    def test_not1(self):
        
        s1 = {'not': {'type': 'integer', 'minimum': 10, 'maximum': 20}}
        s2 = {'not': {'minimum': 10, 'maximum': 20}}

        s1_ = {'anyOf': [{'type': 'boolean'}, {'type': 'object'}, {'type': 'null'}, {'type': 'array'}, {'type': 'string'}, {'maximum': 9, 'type': 'integer'}, {'minimum': 21, 'type': 'integer'}, {
            'type': 'number', 'maximum': 9}, {'type': 'number', 'minimum': 21}, {'allOf': [{'type': 'number', 'minimum': 10, 'maximum': 20}, {'not': {'type': 'integer'}}]}]}

        # with self.subTest('LHS < RHS'):
        #     self.assertFalse(isSubschema(s1, s1))
        # with self.subTest('RHS > LHS'):
        #     self.assertTrue(isSubschema(s2, s1))


class TestCompositeNumericSubtype(unittest.TestCase):

    def test_invalid_schema(self):
        s1 = {"type": "integer"}
        s2 = {"type": "number",
              "allOf": [""]}
        with self.subTest():
            self.assertRaises(SchemaError, isSubschema, s1, s2)
        with self.subTest():
            self.assertRaises(SchemaError, isSubschema, s2, s1)

    def test_int_int_num1(self):
        s1 = {"type": "integer"}
        s2 = {"type": "number",
              "allOf": [{"type": "integer"}, {"type": "number", "minimum": 10}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_int_int_num2(self):
        s1 = {"type": "integer", "multipleOf": 5}
        s2 = {"type": "number",
              "allOf": [{"type": "integer"}, {"type": "number", "minimum": 10}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_int_mul_mul1(self):
        s1 = {"type": "integer", "multipleOf": 5}
        s2 = {"type": "number",
              "multipleOF": 3,
              "allOf": [{"type": "integer"}, {"type": "number", "multipleOf": 3}]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_int_mul_mul2(self):
        s1 = {"type": "integer", "multipleOf": 15}
        s2 = {"type": "number",
              "multipleOf": 3,
              "allOf": [{"type": "integer"}, {"type": "number", "multipleOf": 5}]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_all_all_1(self):
        s1 = {"type": "integer",
              "allOf": [{"multipleOf": 3}, {"minimum": 5}]}  # 6, 9, 12, 15, 18, ...
        s2 = {"type": "number", "multipleOf": 3,
              "allOf": [{"type": "integer"}, {"type": "number", "multipleOf": 5}]}  # ..., -30, -15, 15, 30, 45, ..
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_all_all_2(self):
        s1 = {"type": "integer",
              "allOf": [{"multipleOf": 3}]}
        s2 = {"type": "number", "multipleOf": 3,
              "allOf": [{"type": "integer"}, {"type": "number", "multipleOf": 3}]}  # ..., -30, -15, 15, 30, 45, ..
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_all_all_3(self):
        s1 = {"type": "number", "allOf": [{"multipleOf": .3}]}
        s2 = {"type": "number", "multipleOf": 3,
              "allOf": [{"type": "integer"}, {"type": "number", "multipleOf": 3}]}  # ..., -30, -15, 15, 30, 45, ..
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_enum1(self):
        s1 = {"enum": [1, 2, 3]}
        s2 = {"type": "number"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_enum2(self):
        s1 = {"enum": [1.0, 2, 3]}
        s2 = {"enum": [1, 2.0]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_enum3(self):
        s1 = {"enum": [1, 2, 3]}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_enum4(self):
        s1 = {"enum": [1, 2.0, 3]}
        s2 = {"type": "integer"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))
