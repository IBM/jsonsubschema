'''
Created on June 3, 2019
@author: Andrew Habib
'''

import unittest

from jsonsubschema import isSubschema
from jsonsubschema.exceptions import UnsupportedEnumCanonicalization


class TestEnum(unittest.TestCase):

    def test_enum_simple1(self):
        s1 = {'enum': [1]}
        s2 = {'enum': [1, 2]}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_enum_simple2(self):
        s1 = {'enum': [True]}
        s2 = {'enum': [1, 2]}

        with self.subTest('LHS < RHS'):
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_enum_simple3(self):
        s1 = {'type': 'integer', 'enum': [1, 2]}
        s2 = {'type': 'boolean', 'enum': [True]}

        with self.subTest('LHS < RHS'):
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_enum_simple4(self):
        s1 = {'enum': ['1', 2]}
        s2 = {'enum': [1, '2']}

        with self.subTest('LHS < RHS'):
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_enum_uninhabited1(self):
        s1 = {'type': 'string', 'enum': [1, 2]}
        s2 = {'type': 'string'}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_enum_uninhabited2(self):
        s1 = {'type': 'string', 'enum': [0, 1]}
        s2 = {'type': 'boolean', 'enum': [0]}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertTrue(isSubschema(s2, s1))

    def test_enum_uninhabited3(self):
        s1 = {'enum': []}
        s2 = {'type': 'boolean'}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertFalse(isSubschema(s2, s1))

    def test_enum_uninhabited4(self):
        s1 = {'enum': []}
        s2 = {'not': {}}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest('LHS > RHS'):
            self.assertTrue(isSubschema(s2, s1))


class TestEnumNotSupported(unittest.TestCase):

    def test_array(self):
        s1 = {'enum': [[]]}
        s2 = {'type': 'array'}

        with self.subTest():
            self.assertRaises(UnsupportedEnumCanonicalization,
                              isSubschema, s1, s2)

        with self.subTest():  # To test prining the exception msg
            with self.assertRaises(UnsupportedEnumCanonicalization) as ctxt:
                isSubschema(s2, s1)
            print(ctxt.exception)

    def test_object(self):
        s1 = {'enum': [{'foo': 1}]}
        s2 = {'type': 'object'}

        with self.subTest():
            self.assertRaises(UnsupportedEnumCanonicalization,
                              isSubschema, s1, s2)

        with self.subTest():  # To test prining the exception msg
            with self.assertRaises(UnsupportedEnumCanonicalization) as ctxt:
                isSubschema(s2, s1)
            print(ctxt.exception)
