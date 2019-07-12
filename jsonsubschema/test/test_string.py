'''
Created on July 11, 2019
@author: Andrew Habib
'''

import unittest
import warnings

from jsonschema.exceptions import SchemaError

from checker import isSubschema


class TestStringSubtype(unittest.TestCase):

    def test_min_min(self):
        s1 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "string", "minLength": 5}
        s2 = {"$schema": "http://json-schema.org/draft-04/schema",
              "type": "integer", "maxLength": 1}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

