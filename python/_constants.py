'''
Created on June 7, 2019
@author: Andrew Habib
'''

from intervals import inf as infinity

Jtypes = ["string", "number", "integer", "boolean", "null", "array", "object"]

Jconnectors = ["anyOf", "allOf", "oneOf", "not"]

Jcommonkw = Jconnectors + ["enum", "type"]

JtypesToKeywords = {
    "string": ["minLength", "maxLength", "pattern"],
    "number": ["minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf"],
    "integer": ["minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum", "multipleOf"],
    "boolean": [],
    "null": [],
    "array": ["minItems", "maxItems", "items", "uniqueItems"],
    "object": ["properties", "additionalProperties", "required", "minProperties", "maxProperties", "dependencies", "patternProperties"]
}

JkeywordsToDefaults = {
    "minLength": 0, "maxLength": infinity, "pattern": ".*",

    "minimum": -infinity, "maximum": infinity, "exclusiveMinimum": False, 
    "exclusiveMaximum": False, "multipleOf": 1,
    
    "minItems": 0, "maxItems": infinity, "items": {}, "additionalItems": {},"uniqueItems": False,
    
    "properties": {}, "additionalProperties": {}, "required": [], "minProperties": 0, "maxProperties": infinity, "dependencies": {}, "patternProperties": {}
}