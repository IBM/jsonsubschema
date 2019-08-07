'''
Created on June 24, 2019
@author: Andrew Habib
'''

import json

from jsonsubschema._canoncalization import (
    canonicalize_dict,
    canonicalize_json
)
from jsonsubschema._utils import (
    validate_schema,
    print_db
)


class JSONSubSchemaFactory(json.JSONDecoder):
    ''' A json decoder which embeds subtype checking into the json object.
        This is experimental at the moment. '''

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d):
        return canonicalize_dict(d)


def isSubschema(s1, s2):
    ''' Entry point for schema subtype checking. '''

    # Validate both lhs and rhs schemas before starting the subtype checking.
    # Subtyping of invalid schemas is erroneous.

    validate_schema(s1)
    print_db("LHS", s1)
    s1 = canonicalize_json(s1)
    print_db("LHS_canonical", s1)
    print_db()
    validate_schema(s2)
    print_db("RHS", s2)
    s2 = canonicalize_json(s2)
    print_db("RHS_canonical", s2)

    return s1.isSubtype(s2)
