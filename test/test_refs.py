'''
Created on Oct. 25, 2019
@author: Andrew Habib
'''

import unittest

from jsonsubschema import isSubschema


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
