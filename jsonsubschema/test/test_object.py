'''
Created on July 25, 2019
@author: Andrew Habib
'''

import copy
import unittest

from jsonsubschema.checker import isSubschema


class TestObjectSubtype(unittest.TestCase):

    def test_identity(self):
        s1 = {
            "$schema": "http://json-schema.org/draft-04/schema",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"}
            }
        }
        s2 = s1
        self.assertTrue(isSubschema(s1, s2))

    def test_simple_obj1(self):
        s1 = {
            "$schema": "http://json-schema.org/draft-04/schema",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"}
            }
        }
        s2 = copy.deepcopy(s1)
        del s2["properties"]["email"]
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        # with self.subTest():
        #     self.assertFalse(isSubschema(s2, s1))
