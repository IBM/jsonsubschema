'''
Created on May 17, 2019
@author: Andrew Habib
'''

import json
import sys

import jsonschema
import warnings

from _normalizer import lazy_normalize
from _utils import(
     print_db,
     get_types_or_implicit_types
)


class Checker(object):
    # Change here which validator to use.
    VALIDATOR = jsonschema.Draft4Validator

    '''
    The checker class constructor accepts two 'valid' json files.
    '''

    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
        #
        self.validate_schemas()

    def validate_schemas(self):
        '''
        Validate given schemas against the pre-defined VALIDATOR schema.
        '''
        print_db("Validating lhs schema ...")
        Checker.VALIDATOR.check_schema(self.s1)
        #
        print_db("Validating rhs schema ...")
        Checker.VALIDATOR.check_schema(self.s2)

    def is_subschema(self):
        return Checker.is_subtype(self.s1, self.s2)

    @staticmethod
    def is_subtype(s1, s2):
        '''
        Is s1 <: s2 ?
        '''
        
        # Trivial cases + normalization
        # -- case rhs allows anything
        if s2 is True or s2 == {}:
            # warnings.warn(
            #     message="Warning: any schema is sub-schema of True or the empty schema {}. This will always be true.", stacklevel=1)
            return True
        # -- case lhs == rhs
        if s1 == s2:
            # warnings.warn(
            #     message="Warning: any schema is sub-schema of itself. This will always be true.", stacklevel=1)
            return True
        # -- case rhs does not allow anything
        if s2 is False or s2.get("not") == {}:
            # warnings.warn(
            #     message="Warning: No schema is sub-schema of False or the ~ empty schema 'not': {}. This will always be false.", stacklevel=1)
            return False

        # normalization
        print_db(s1)
        s1 = lazy_normalize(s1)
        print_db(s1)
        
        print_db(s2)
        s2 = lazy_normalize(s2)
        print_db(s2)
        #
        # t1_orig = set(s1.get("type"))
        # t2_orig = set(s2.get("type"))
        # t1_isExplicit = True if s1.get("type") else False
        # t2_isExplicit = True if s2.get("type") else False
        
        # t1 = get_types_or_implicit_types(s1)
        # t2 = get_types_or_implicit_types(s2)
        # t1_overlap_t2 = set(t1) & set(t2)

        # if (JsonNumeric.NAMES & set(t1)) and (JsonNumeric.NAMES & set(t2)) and (not t1_overlap_t2):
        #     t1_overlap_t2.add(JsonNumeric.NAME)
        
        # if t1_isExplicit and t2_isExplicit:
        #     if not t1_overlap_t2 or \
        #         t1_overlap_t2 and len(t1_overlap_t2) < len(t1):
        #         return False
        
        # elif not t1_isExplicit and not t2_isExplicit:    
        #     if not t1_overlap_t2:
        #         return True
        
        # elif t1_isExplicit and not t2_isExplicit:
        #     if not t1_overlap_t2:
        #         return True

        # elif not t1_isExplicit and t2_isExplicit:
        #     if not t1_overlap_t2:
        #         return False
            
        # build explicit types based on type-related key words
        # s1["type"] = t1
        # s2["type"] = t2

        from checkers import JSON_SUBTYPE_CHECKERS
        print_db("-->", s1)
        print_db("-->", s2)
        # Gonna give higher precedence to boolean connectors over
        # 'type' cuz the connectors condition has to be met anyways.
        if "anyOf" in s1.keys():
            return JSON_SUBTYPE_CHECKERS.get("anyOf")(s1, s2)
        elif "anyOf" in s2.keys():
            return JSON_SUBTYPE_CHECKERS.get("anyOf_rhs")(s1, s2)

        else:
            return JSON_SUBTYPE_CHECKERS.get(s1["type"])(s1, s2)

        # results = []
        # for t in t1_overlap_t2:
        #     results.append(JSON_SUBTYPE_CHECKERS.get(t)(s1, s2))
        # if all(results):
        #     return True
        # else: 
        #     return False



if __name__ == "__main__":
    '''
    Accepts two arguments s1 and s2.
    Checks wther s1 <: s2
    '''
    if len(sys.argv) != 3:
        print("Wrong arguments: accepts two .json schema files.")
        sys.exit()

    s1_file = sys.argv[1]
    s2_file = sys.argv[2]

    print("Loading json schemas from:\n{}\n{}\n".format(s1_file, s2_file))
    with open(s1_file, 'r') as f1:
        s1 = json.load(f1)
    with open(s2_file, 'r') as f2:
        s2 = json.load(f2)

    checker = Checker(s1, s2)
    print(checker.is_subschema())
