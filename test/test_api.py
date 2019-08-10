'''
Created on August 9, 2019
@author: Andrew Habib
'''

import json
import unittest

import jsonsubschema._checkers as c
from jsonsubschema.api import *

s1 = {"type": "number"}
s2 = {"type": "integer"}

s_1 = '{"type": "number"}'
s_2 = '{"type": "integer"}'

class TestAPI(unittest.TestCase):

    def test_decoder_and_api(self):
        s1 = json.loads(s_1, cls=JSONSubSchemaFactory)
        s2 = json.loads(s_2, cls=JSONSubSchemaFactory)

        with self.subTest():
            self.assertFalse(s1.isSubtype(s2))
        with self.subTest():
            self.assertTrue(s2.isSubtype(s1))
        #
        with self.subTest():
            self.assertEqual(s1.meet(s1), s1)
        
        with self.subTest():
            self.assertEqual(s2.meet(s2), s2)
        
        with self.subTest():
            self.assertEqual(s1.meet(s2), s2.meet(s1), c.JSONTypeInteger({}))
        #
        with self.subTest():
            self.assertEqual(s1.join(s1), join(s1, s1), s1)
        
        with self.subTest():
            self.assertEqual(s2.join(s2), join(s2, s2), s2)
        
        with self.subTest():
            self.assertEqual(s1.join(s2), s2.join(s1))
        #
        with self.subTest():
            self.assertTrue((s1.meet(s2)).isSubtype(s2.meet(s1)))

        with self.subTest():
            self.assertTrue((s2.meet(s1)).isSubtype(s1.meet(s2)))
        #
        with self.subTest():
            self.assertTrue((s1.join(s2)).isSubtype(s2.join(s1)))

        with self.subTest():
            self.assertTrue((s2.join(s1)).isSubtype(s1.join(s2)))

    def test_api_isSubschema(self):
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))
        
        with self.subTest():
            self.assertTrue(isSubschema(join(s1, s2), join(s2, s1)))
        with self.subTest():
            self.assertTrue(isSubschema(meet(s1, s2), meet(s2, s1)))

        with self.subTest():
            self.assertTrue(isSubschema(meet(s1, s2), join(s2, s1)))
        with self.subTest():
            self.assertFalse(isSubschema(join(s1, s2), meet(s2, s1)))

    def test_api_meet(self):
        with self.subTest():
            self.assertEqual(meet(s1, s2), meet(s2, s1), c.JSONTypeInteger({}))
        
        with self.subTest():
            self.assertEqual(meet(s1, s1), s1)
        with self.subTest():
            self.assertEqual(meet(s2, s2), s2)

    def test_api_join(self):
        with self.subTest():
            self.assertEqual(join(s1, s2), join(s2, s1))
        
        # with self.subTest():
        #     self.assertEqual(join(s1, s1), s1)
        # with self.subTest():
        #     self.assertEqual(join(s2, s2), s2)
