'''
Created on June 3, 2019
@author: Andrew Habib
'''

import unittest

from jsonsubschema import isSubschema


class TestSingletonBooleans(unittest.TestCase):

    def test_oneOf(self):
        s1 = {'oneOf': [{'type': 'string'}]}
        s2 = {'type': 'string'}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_anyOf(self):
        s1 = {'anyOf': [{'type': 'string'}]}
        s2 = {'type': 'string'}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_allOf(self):
        s1 = {'allOf': [{'type': 'string'}]}
        s2 = {'type': 'string'}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_allOf_oneOf(self):
        s1 = {'allOf': [{'type': 'string'}]}
        s2 = {'oneOf': [{'type': 'string'}]}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))


class TestOneOf(unittest.TestCase):

    def test_oneof1(self):
        # equiv to {'not': {string}}
        s1 = {'oneOf': [{'type': 'string'}, {}]}
        s2 = {'type': 'string'}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_oneof2(self):
        # equiv to {'not': {string}}
        s1 = {'oneOf': [{'type': 'string'}, {}]}
        s2 = {'not': {'type': 'string'}}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_oneof4(self):
        s1 = {'oneOf': [{'type': 'boolean'}, {'enum': [True]}]}
        s2 = {'enum': [False]}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_oneOf5(self):
        # accepts 3 only
        s1 = {'oneOf': [{'enum': [1, 2, 3]}, {'enum': [1, 2]}]}
        s2 = {'enum': [3]}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertTrue(isSubschema(s2, s1))

    def test_oneOf6(self):
        # accepts 3 only
        s1 = {'oneOf': [{'enum': [1, 2, 3]}, {'enum': [1, 2]}]}
        s2 = {'enum': [1, 2]}

        with self.subTest('LHS < RHS'):
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))


class TestAllOf(unittest.TestCase):

    def test_allOf1(self):
        s1 = {'allOf': [{'type': 'string'}, {
            'type': 'string', 'pattern': 'a'}]}
        s2 = {'type': 'string'}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_allOf2(self):
        s1 = {'allOf': [{'minimum': 10}, {'maximum': 20}]}
        s2 = {'minimum': 10, 'maximum': 20}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertTrue(isSubschema(s2, s1))


class TestNotBoolean(unittest.TestCase):

    def test_not_allOf1(self):
        s1 = {'not': {'allOf': [{'type': 'string'},
                                {'type': 'string', 'pattern': 'a'}]}}
        s2 = {'type': 'string'}

        with self.subTest('LHS < RHS'):
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_not_allOf2(self):
        s1 = {'not': {'allOf': [{'type': 'string'},
                                {'type': 'string', 'pattern': 'a'}]}}
        s2 = {'anyOf': [{'type': 'integer'}, {'type': 'number'}, {'type': 'boolean'}, {
            'type': 'array'}, {'type': 'object'}, {'type': 'string'}, {'type': 'null'}]}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_not_allOf3(self):
        s1 = {'not': {'allOf': [{'type': 'string'},
                                {'type': 'string', 'pattern': 'a'}]}}
        s2 = {'anyOf': [{'type': 'integer'}, {'type': 'number'}, {'type': 'boolean'}, {'type': 'array'}, {
            'type': 'object'}, {'type': 'string', 'pattern': '^[^a]*$'}, {'type': 'null'}]}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertTrue(isSubschema(s2, s1))

    def test_not_allOf4(self):
        s1 = {'not': {'allOf': [{'type': 'string'}, {'type': 'boolean'}]}}
        s2 = {}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertTrue(isSubschema(s2, s1))

    def test_not_anyOf1(self):
        s1 = {'not': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}}
        s2 = {'type': 'string'}

        with self.subTest('LHS < RHS'):
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_not_anyOf2(self):
        s1 = {'not': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}}
        s2 = {'anyOf': [{'type': 'integer'}, {'type': 'number'}, {'type': 'boolean'}, {'type': 'array'}, {
            'type': 'object'}, {'type': 'string'}, {'type': 'null'}]}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_not_oneOf1(self):
        s1 = {'not': {'oneOf': [{'type': 'string'}, {'type': 'null'}]}}
        s2 = {'type': 'string'}

        with self.subTest('LHS < RHS'):
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_not_oneOf2(self):
        # accepts anything but 3
        s1 = {'not': {'oneOf': [{'enum': [1, 2, 3]}, {'enum': [1, 2]}]}}
        s2 = {'not': {'enum': [3]}}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertTrue(isSubschema(s2, s1))


class TestNotBooleans(unittest.TestCase):

    def test_not_and_allOf1(self):
        s1 = {'not': {'type': 'string'},
              'allOf': [{'type': 'integer'}, {'enum': [5]}]}
        s2 = {'enum': [5]}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertTrue(isSubschema(s2, s1))

    def test_not_and_anyOf1(self):
        s1 = {'not': {'type': 'string'},
              'anyOf': [{'type': 'integer'}, {'type': 'boolean'}]}
        s2 = {'type': ['integer', 'boolean']}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertTrue(isSubschema(s2, s1))

    def test_not_and_two_booleans(self):
        s1 = {'not': {'type': 'string'},
              'anyOf': [{'type': 'integer'}, {'type': 'boolean'}],
              'allOf': [{'minimum': 10}]}

        s2 = {'type': ['integer', 'boolean']}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_not_and_two_nested_booleans(self):
        s1 = {'not': {'anyOf': [{'type': 'integer'}, {'type': 'boolean'}], 'allOf': [
            {'minimum': 10}, {'maximum': 20}]}}

        s2 = {'not': {'type': ['integer', 'boolean'],
                      'minimum': 10, 'maximum': 20}}

        # with self.subTest('LHS < RHS'):
        #     self.assertTrue(isSubschema(s1, s2))
        # with self.subTest('LHS > RHS'):
        #     self.assertTrue(isSubschema(s2, s1))

    def test_two_booleans(self):
        s1 = {'anyOf': [{'type': 'integer'}, {'type': 'boolean'}], 'allOf': [
            {'minimum': 10}, {'maximum': 20}]}

        s2 = {'type': ['integer', 'boolean'], 'minimum': 10, 'maximum': 20}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertTrue(isSubschema(s2, s1))
