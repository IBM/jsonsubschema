'''
Created on June 7, 2019
@author: Andrew Habib
'''

from intervals import inf as infinity

Jnumeric = set(["integer", "number"])

Jtypes = set(["string", "boolean", "null", "array", "object"]).union(Jnumeric)

Jconnectors = set(["anyOf", "allOf", "oneOf", "not"])

Jtypecommonkw = Jconnectors.union(["enum", "type"])

JtypesToKeywords = {
    "string": ["minLength", "maxLength", "pattern"],
    "number": ["minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf"],
    "integer": ["minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf"],
    "boolean": [],
    "null": [],
    "array": ["minItems", "maxItems", "items", "additionalItems", "uniqueItems"],
    "object": ["properties", "additionalProperties", "required", "minProperties", "maxProperties", "dependencies", "patternProperties"]
}

JkeywordsToDefaults = {
    "minLength": 0, "maxLength": infinity, "pattern": ".*",
    "minimum": -infinity, "maximum": infinity, "exclusiveMinimum": False, "exclusiveMaximum": False, "multipleOf": None,
    "minItems": 0, "maxItems": infinity, "items": {}, "additionalItems": {}, "uniqueItems": False,
    "properties": {}, "additionalProperties": {}, "required": [], "minProperties": 0, "maxProperties": infinity, "dependencies": {}, "patternProperties": {}
}

Jmeta = set(["$schema", "$id", "$ref"])

Jkeywords_lhs = Jtypecommonkw.union(Jconnectors, JkeywordsToDefaults.keys())

Jkeywords = Jtypes.union(Jtypecommonkw)

Jkeywords = Jkeywords.union(JkeywordsToDefaults.keys())
