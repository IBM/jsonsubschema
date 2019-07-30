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
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"}
            }
        }
        s2 = copy.deepcopy(s1)
        s2["properties"]["gender"] = {
            "type": "string", "maxLength": 1, "enum": ["M", "F"]}
        self.assertTrue(isSubschema(s1, s2))

    def test_min_property(self):
        s1 = {"type": "object", "minProperties": 1}
        s2 = {"type": "object"}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_max_property(self):
        s1 = {"type": "object", "maxProperties": 3}
        s2 = {"type": "object"}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_property1(self):
        s1 = {"type": "object", "minProperties": 1, "maxProperties": 3}
        s2 = {"type": "object"}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_property2(self):
        s1 = {"type": "object", "minProperties": 1, "maxProperties": 3}
        s2 = {"type": "object", "maxProperties": 5}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_min_max_property3(self):
        s1 = {"type": "object", "minProperties": 1, "maxProperties": 3}
        s2 = {"type": "object", "minProperties": 5, "maxProperties": 2}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_min_max_property4(self):
        s1 = {"type": "object", "minProperties": 1, "maxProperties": 10}
        s2 = {"type": "object", "minProperties": 2, "maxProperties": 5}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_required1(self):
        s1 = {"type": "object", "minProperties": 1}
        s2 = {"type": "object", "required": ["p1"]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_require2(self):
        s1 = {"type": "object", "minProperties": 1}
        s2 = {"type": "object", "required": ["p1", "p2"]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_require3(self):
        s1 = {"type": "object", "maxProperties": 1}
        s2 = {"type": "object", "required": ["p1", "p2"]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_require4(self):
        s1 = {"type": "object", "required": ["p2", "p1"]}
        s2 = {"type": "object", "required": ["p1", "p2"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_require5(self):
        s1 = {"type": "object", "required": ["p1"]}
        s2 = {"type": "object", "required": ["p2"]}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_require6(self):
        s1 = {"type": "object", "required": ["p1", "p2"]}
        s2 = {"type": "object", "required": ["p2"]}
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_require7(self):
        s1 = {"type": "object", "required": ["p1", "p2"]}
        s2 = {"type": "object", "required": [
            "p2"], "additionalProperties": {"type": "boolean"}}
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_simple_obj1(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
            }
        }
        s2 = copy.deepcopy(s1)
        del s2["properties"]["email"]
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_simple_obj2(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
            }
        }
        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
            },
            "patternProperties": {
                "^b.*b$": {"type": "boolean"}
            }
        }
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_simple_obj3(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
            },
            "patternProperties": {
                "b.*b": {"type": "boolean"}
            }
        }
        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
            },
            "patternProperties": {
                "^ba+b$": {"type": "boolean"}
            }
        }
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_simple_obj4(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
            },
            "patternProperties": {
                "b.*b": {"type": "integer"}
            }
        }
        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
            },
            "patternProperties": {
                "^ba+b$": {"type": "boolean"}
            }
        }
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_tricky1(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
                "emaik": {"type": "string", "format": "email"}
            }
        }
        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]}
            },
            "patternProperties": {
                "^emai(l|k)$": {"type": "string"}
            },
            "required": ["name"]
        }
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_tricky2(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
                "emaik": {"type": "string", "format": "email"}
            }
        }
        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]}
            },
            "patternProperties": {
                "^emai(l|k)$": {"type": "string"}
            }
        }
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_tricky3(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
                "emaik": {"type": "string", "format": "email"}
            }
        }
        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]}
            },
            "patternProperties": {
                "emai": {"type": "string"}
            }
        }
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_tricky4(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
                "emaik": {"type": "string", "format": "email"}
            }
        }
        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]}
            },
            "patternProperties": {
                "emai": {"type": "string", "minLength": 10}
            }
        }
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertTrue(isSubschema(s2, s1))

    def test_tricky5(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
                "emaik": {"type": "string", "format": "email"}
            },
            "additionalProperties": {"type": "boolean"}
        }
        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]}
            },
            "patternProperties": {
                "emai": {"type": "string", "minLength": 10}
            }
        }
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_tricky6(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
                "emaik": {"type": "string", "format": "email"}
            },
            "additionalProperties": {"type": "boolean"}
        }
        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]}
            },
            "patternProperties": {
                "emai": {"type": "string", "minLength": 10}
            },
            "additionalProperties": {"type": "boolean"}
        }
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

    def test_tricky7(self):
        s1 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]},
                "email": {"type": "string", "format": "email"},
                "emaik": {"type": "string", "format": "email"}
            },
            "additionalProperties": {"type": "string"}
        }

        s2 = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "gender": {"type": "string", "maxLength": 1, "enum": ["F", "M"]}
            },
            "patternProperties": {
                "emai": {"type": "string"}
            }

        }
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))
