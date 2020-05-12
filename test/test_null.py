'''
Created on June 3, 2019
@author: Andrew Habib
'''

import unittest

from jsonsubschema import isSubschema


class TestNull(unittest.TestCase):

    def test_null1(self):
        s1 = {'enum': [None]}
        s2 = {'type': 'null'}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_null2(self):
        s1 = {'type': 'null'}
        s2 = {}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_null3(self):
        s1 = {'enum': [None]}
        s2 = {'enum': [0]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))
