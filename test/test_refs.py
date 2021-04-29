'''
Created on Oct. 25, 2019
@author: Andrew Habib
'''

import unittest

from jsonsubschema import isSubschema
from jsonsubschema.exceptions import UnsupportedRecursiveRef


class TestSimpleRefs(unittest.TestCase):

    def test_1(self):
        s1 = {'definitions': {'bom': {'type': 'string'},
                              'tak': {'type': 'integer'}},
              'type': 'object', 'properties':
              {'foo': {'$ref': '#/definitions/bom',
                       'type': 'integer'}}}
        s2 = {'type': 'object',
              'properties': {
                  'foo': {'type': 'string'}}}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_2(self):
        s1 = {'definitions': {'bom': {'type': 'string'},
                              'tak': {'type': 'integer'}},
              'type': 'object', 'properties':
              {'foo': {'$ref': '#/definitions/bom',
                       'type': 'integer'}}}
        s2 = {'type': 'object',
              'properties': {
                  'foo': {'type': 'string', 'pattern': 'a'}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))


class TestRefs(unittest.TestCase):

    def test_1(self):
        s1 = {
            "type": "array",
            "items": {"$ref": "#/definitions/positiveInteger"},
            "definitions": {
                "positiveInteger": {
                    "type": "integer",
                    "minimum": 0,
                    "exclusiveMinimum": True
                }
            }
        }
        s2 = {
            "type": "array",
            "items": {"$ref": "#/definitions/positiveInteger"},
            "definitions": {
                "positiveInteger": {
                    "type": "integer",
                    "minimum": -1,
                    "exclusiveMinimum": True
                }
            }
        }
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

        s3 = {"type": "array", "items": {"type": "integer"}}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s3))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s3))

        s4 = {"type": "array", "items": {"type": "string"}}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s4))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s4))

        s4 = {"type": "string"}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s4))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s4))

    @unittest.skip("Recursive schema; fails due to jsonschema failure case, not us")
    def test_2(self):
        s1 = {"definitions": {"S": {"anyOf": [{"enum": [None]},
                                              {"allOf": [{"items": [{"$ref": "#/definitions/S"},
                                                                    {"$ref": "#/definitions/S"}],
                                                          "maxItems": 2,
                                                          "minItems": 2,
                                                          "type": "array"},
                                                         {"not": {"type": "array",
                                                                  "uniqueItems": True}}
                                                         ]
                                               }
                                              ]
                                    }
                              },
              "$ref": "#/definitions/S"
              }

        s2 = {"enum": [None]}

        with self.subTest():
            with self.assertRaises(UnsupportedRecursiveRef) as ctxt:
                isSubschema(s2, s1)
            print(ctxt.exception)

    def test_3(self):
        s1 = {
            "definitions": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "children": {
                            "type": "array",
                            "items": {"$ref": "#/definitions/person"},
                            "default": []
                        }
                    }
                }
            },
            "type": "object",
            "properties": {
                "person": {"$ref": "#/definitions/person"}
            }
        }

        s2 = {"enum": [None]}

        with self.subTest():
            with self.assertRaises(UnsupportedRecursiveRef) as ctxt:
                isSubschema(s2, s1)
            print(ctxt.exception)
