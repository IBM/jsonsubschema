'''
Created on June 24, 2019
@author: Andrew Habib
'''

import json
import jsonref

from jsonsubschema._canonicalization import (
    canonicalize_schema,
    simplify_schema_and_embed_checkers
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
        return simplify_schema_and_embed_checkers(
            canonicalize_schema(d))


def prepare_operands(s1, s2):
    # First, we reload schemas using jsonref to resolve $ref
    # before starting canonicalization.
    # At the moment, we will get undefined behaviour for recursive/circual refs.

    # s1 = jsonref.loads(json.dumps(s1))
    # s2 = jsonref.loads(json.dumps(s2))
    # This is not very efficient, should be done lazily maybe?
    s1 = jsonref.JsonRef.replace_refs(s1)
    s2 = jsonref.JsonRef.replace_refs(s2)

    # Canonicalize and embed checkers for both lhs
    # and rhs schemas  before starting the subtype checking.
    # This also validates input schemas and canonicalized schemas.

    print_db("LHS", s1)
    print_db()
    s1 = simplify_schema_and_embed_checkers(
        canonicalize_schema(s1))
    print_db("LHS_canonical", s1)
    print_db()

    print_db("RHS", s2)
    print_db()
    s2 = simplify_schema_and_embed_checkers(
        canonicalize_schema(s2))
    print_db("RHS_canonical", s2)
    print_db()
    return s1, s2


def isSubschema(s1, s2):
    ''' Entry point for schema subtype checking. '''
    s1, s2 = prepare_operands(s1, s2)
    return s1.isSubtype(s2)


def meet(s1, s2):
    ''' Entry point for schema meet operation. '''
    s1, s2 = prepare_operands(s1, s2)
    return s1.meet(s2)


def join(s1, s2):
    ''' Entry point for schema meet operation. '''
    s1, s2 = prepare_operands(s1, s2)
    return s1.join(s2)


def isEquivalent(s1, s2):
    ''' Entry point for schema equivalence check operation. '''
    return isSubschema(s1, s2) and isSubschema(s2, s1)
