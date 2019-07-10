'''
Created on June 24, 2019
@author: Andrew Habib
'''

import copy
import json

from _canoncalization import (
    canoncalize_dict,
    canoncalize_json
)
from _utils import (
    print_db,
    validate_schema
)


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

    print_db(s1)
    print_db(s2)

    # copy original json dicts becuase
    # we heavily modify the json object.
    s1_ = copy.deepcopy(s1)
    s2_ = copy.deepcopy(s2)

    validate_schema(s1_)
    validate_schema(s2_)

    s1_ = canoncalize_json(s1_)
    s2_ = canoncalize_json(s2_)

    print_db(s1_)
    print_db(s2_)
    return s1_.isSubtype(s2_)
