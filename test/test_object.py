'''
Created on July 25, 2019
@author: Andrew Habib
'''

import copy
import unittest

from jsonsubschema import isSubschema


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

    def test_simple_obj5(self):
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
                "^b(\w)+b$": {"type": "integer", "minimum": 10}
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

    def test_required_with_real_schema(self):
        s1 = {'additionalProperties': False,
              'properties': {'X': {'$schema': 'http://json-schema.org/draft-04/schema#',
                                   'items': {'items': {'type': 'number'},
                                             'maxItems': 4,
                                             'minItems': 4,
                                             'type': 'array'},
                                   'maxItems': 150,
                                   'minItems': 150,
                                   'type': 'array'},
                             'y': {'$schema': 'http://json-schema.org/draft-04/schema#',
                                   'items': {'type': 'integer'},
                                   'maxItems': 150,
                                   'minItems': 150,
                                   'type': 'array'}},
              'required': ['X', 'y'],
              'type': 'object'}

        s2 = {'$schema': 'http://json-schema.org/draft-04/schema#',
              'additionalProperties': False,
              'description': 'Input data schema for training.',
              'properties': {'X': {'description': 'Features; the outer array is '
                                   'over samples.',
                                   'items': {'items': {'type': 'number'},
                                             'type': 'array'},
                                   'type': 'array'},
                             'y': {'description': 'Target class labels; the array '
                                   'is over samples.',
                                   'items': {'type': 'number'},
                                   'type': 'array'}},
              'required': ['X', 'y'],
              'type': 'object'}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))


    def test_real_object_schema(self):
        s1 = {'additionalProperties': False,
              'properties': {'X': {'$schema': 'http://json-schema.org/draft-04/schema#',
                                   'items': {'items': [
                                                        {'description': 'sepal length (cm)',
                                                        'type': 'number'},
                                                       {'description': 'sepal width (cm)',
                                                        'type': 'number'},
                                                       {'description': 'petal length (cm)',
                                                        'type': 'number'},
                                                       {'description': 'petal width (cm)',
                                                        'type': 'number'}
                                                        ],
                                             'maxItems': 4,
                                             'minItems': 4,
                                             'type': 'array'},
                                   'maxItems': 120,
                                   'minItems': 120,
                                   'type': 'array'},
                             'y': {'$schema': 'http://json-schema.org/draft-04/schema#',
                                   'items': {'description': 'target',
                                             'type': 'integer'},
                                   'maxItems': 120,
                                   'minItems': 120,
                                   'type': 'array'}},
              'required': ['X', 'y'],
              'type': 'object'}

        s2 = {'$schema': 'http://json-schema.org/draft-04/schema#',
              'additionalProperties': False,
              'description': 'Input data schema for training.',
              'properties': {'X': {'description': 'Features; the outer array is over samples.',
                                   'items': {'items': {'type': 'number'},
                                             'type': 'array'},
                                   'type': 'array'},
                             'y': {'description': 'Target class labels; the array is over samples.',
                                   'items': {'type': 'number'},
                                   'type': 'array'}},
              'required': ['X', 'y'],
              'type': 'object'}

        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))
        with self.subTest():
            self.assertFalse(isSubschema(s2, s1))

class TestDependency(unittest.TestCase):

    def test_1(self):
        s1 = {'type': 'object', 'dependencies': {'foo': {'type':'string'}}}
        s2 = {'type': 'object'}

        with self.subTest('LHS < RHS'):
            self.assertTrue(isSubschema(s1, s2))
        # with self.subTest('"dependencies" not yet supported.'):
        #     self.assertFalse(isSubschema(s2, s2))