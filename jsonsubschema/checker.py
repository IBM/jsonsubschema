'''
Created on June 24, 2019
@author: Andrew Habib
'''

import json

from _canoncalization import (
    canoncalize_dict,
    canoncalize_json
)
from _utils import validate_schema


class JSONSubSchemaFactory(json.JSONDecoder):
    ''' This is a json decoder which allows subtype checking.
        Not recommended, however, due to the inability to properly 
        validate the schema before starting the type checking. '''

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d):
        return canoncalize_dict(d)


def isSubschema(s1, s2):
    ''' Entry point for schema subtype checking. '''
    validate_schema(s1)
    validate_schema(s2)
    s1 = canoncalize_json(s1)
    s2 = canoncalize_json(s2)
    return s1.isSubtype(s2)
