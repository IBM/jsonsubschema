'''
Created on April 24, 2020
@author: Andrew Habib
'''

import unittest

from jsonschema import SchemaError

from jsonsubschema import isSubschema


class TestUnknownTypes(unittest.TestCase):

    def test_single_type(self):
        s1 = {'type': 'foo'}
        s2 = {}

        with self.subTest():
            self.assertRaises(SchemaError, isSubschema, s1, s2)

    def test_list_of_types(self):
        s1 = {'type': ['foo', 'string']}
        s2 = {}

        with self.subTest():
            self.assertRaises(SchemaError, isSubschema, s1, s2)
