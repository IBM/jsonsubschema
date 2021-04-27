'''
Created on August 9, 2019
@author: Andrew Habib
'''

import json
import unittest

import jsonsubschema._checkers as c
from jsonsubschema import *
from jsonsubschema._canonicalization import *

s1 = {"type": "number"}
s2 = {"type": "integer"}

s_1 = '{"type": "number"}'
s_2 = '{"type": "integer"}'


class TestAPI(unittest.TestCase):

    def test_decoder_and_api(self):

        s1 = simplify_schema_and_embed_checkers(
            canonicalizeSchema(json.loads(s_1)))
        s2 = simplify_schema_and_embed_checkers(
            canonicalizeSchema(json.loads(s_2)))

        with self.subTest():
            self.assertFalse(s1.isSubtype(s2))

        with self.subTest():
            self.assertTrue(s2.isSubtype(s1))

        with self.subTest():
            self.assertEqual(s1.meet(s1), s1)

        with self.subTest():
            self.assertEqual(s2.meet(s2), s2)

        with self.subTest():
            self.assertEqual(s1.meet(s2), s2.meet(s1), c.JSONTypeInteger({}))

        with self.subTest():
            self.assertEqual(s1.join(s1), joinSchemas(s1, s1), s1)

        with self.subTest():
            self.assertEqual(s2.join(s2), joinSchemas(s2, s2), s2)

        with self.subTest():
            self.assertTrue(isEquivalent(s1.join(s2), s2.join(s1)))

        with self.subTest():
            self.assertTrue((s1.meet(s2)).isSubtype(s2.meet(s1)))

        with self.subTest():
            self.assertTrue((s2.meet(s1)).isSubtype(s1.meet(s2)))

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
            self.assertTrue(isSubschema(
                joinSchemas(s1, s2), joinSchemas(s2, s1)))

        with self.subTest():
            self.assertTrue(isSubschema(
                meetSchemas(s1, s2), meetSchemas(s2, s1)))

        with self.subTest():
            self.assertTrue(isSubschema(
                meetSchemas(s1, s2), joinSchemas(s2, s1)))

        with self.subTest():
            self.assertFalse(isSubschema(
                joinSchemas(s1, s2), meetSchemas(s2, s1)))

    def test_api_meet(self):

        with self.subTest():
            self.assertEqual(meetSchemas(s1, s2), meetSchemas(
                s2, s1), c.JSONTypeInteger({}))

        with self.subTest():
            self.assertEqual(meetSchemas(s1, s1), s1)

        with self.subTest():
            self.assertEqual(meetSchemas(s2, s2), s2)

    def test_api_join(self):

        with self.subTest():

            self.assertTrue(isEquivalent(
                joinSchemas(s1, s2), joinSchemas(s2, s1)))

        with self.subTest():
            self.assertEqual(joinSchemas(s1, s1), s1)

        with self.subTest():
            self.assertEqual(joinSchemas(s2, s2), s2)
