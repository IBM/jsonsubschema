'''
Created on August 9, 2019
@author: Andrew Habib
'''

import json
import unittest

import jsonsubschema._checkers as c
from jsonsubschema.api import *

s_1 = '{"type": "number"}'
s_2 = '{"type": "integer"}'

class TestAPI(unittest.TestCase):

    def test_decoder_and_api(self):
        s1 = '{"type": "number"}'
        s2 = '{"type": "integer"}'
        
        s1 = json.loads(s1, cls=JSONSubSchemaFactory)
        s2 = json.loads(s2, cls=JSONSubSchemaFactory)

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

        with self.subTest():
            self.assertFalse(s1.isSubtype(s2))
        with self.subTest():
            self.assertTrue(s2.isSubtype(s1))
        
        with self.subTest():
            self.assertEqual(s1.meet(s1), meet(s1, s1), s1)
        
        with self.subTest():
            self.assertEqual(s2.meet(s2), meet(s2, s2), s2)

        with self.subTest():
            self.assertEqual(s1.meet(s2), s2.meet(s1), c.JSONTypeInteger({}))

        with self.subTest():
            self.assertEqual(meet(s1, s2), meet(s2, s1), c.JSONTypeInteger({}))

        with self.subTest():
            self.assertEqual(s1.join(s1), join(s1, s1), s1)
        
        with self.subTest():
            self.assertEqual(s2.join(s2), join(s2, s2), s2)

        with self.subTest():
            self.assertEqual(s1.join(s2), s2.join(s1), c.JSONanyOf({"anyOf": [s1, s2]}))

        with self.subTest():
            self.assertEqual(join(s1, s2), join(s2, s1), c.JSONanyOf({"anyOf": [s1, s2]}))

    def test_api(self):
        s1 = {"type": "number"}
        s2 = {"type": "integer"}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

        with self.subTest():
            self.assertEqual(meet(s1, s2), meet(s2, s1), c.JSONTypeInteger({}))

        with self.subTest():
            self.assertEqual(join(s1, s2), join(s2, s1), c.JSONanyOf({"anyOf": [s1, s2]}))