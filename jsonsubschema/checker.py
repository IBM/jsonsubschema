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

    # copy original json dict becuase
    # we heavily modify the json object.

    validate_schema(s1)
    print_db("LHS", s1)
    s1_ = copy.deepcopy(s1)
    s1_ = canoncalize_json(s1_)
    print_db("LHS_canonical", s1_)

    validate_schema(s2)
    print_db("RHS", s2)
    s2_ = copy.deepcopy(s2)
    s2_ = canoncalize_json(s2_)
    print_db("RHS_canonical", s2_)

    return s1_.isSubtype(s2_)
