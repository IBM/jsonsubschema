'''
Created on May 17, 2019
@author: Andrew Habib
'''

import json
import sys

import jsonschema
import warnings

from _types import JSON_TYPES, JsonNumeric
from _utils import(
     print_db,
     build_explicit_type_list
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
        # print("Is")
        # print(s1)
        # print("subschema of")
        # print(s2)
        # print()

        # Trivial cases + normalization
        # -- case rhs allows anything
        if s2 is True or s2 == {}:
            warnings.warn(
                message="Warning: any schema is sub-schema of True or the empty schema {}. This will always be true.", stacklevel=1)
            return True
        # -- case rhs does not allow anything
        if s2 is False or s2.get("not") == {}:
            warnings.warn(
                message="Warning: No schema is sub-schema of False or the ~ empty schema 'not': {}. This will always be false.", stacklevel=1)
            return False
        # -- case lhs == rhs
        if s1 == s2:
            warnings.warn(
                message="Warning: any schema is sub-schema of itself. This will always be true.", stacklevel=1)
            return True
        # -- case lhs allowsanthing and rhs is non-empty schema
        if s1 is True or s1 == {} and not s2:
            return False
        # -- case TODO False <: False ?

        # normalization
        
        # True \equiv {}
        if s1 == True:
            s1 = {}
    
        # build explicit types based on type-related key words
        s1["type"] = build_explicit_type_list(s1)
        s2["type"] = build_explicit_type_list(s2)

        # Real stuff
        from _types import JSON_TYPES, JSON_TYPES
        t1 = set(s1.get("type"))
        t2 = set(s2.get("type"))
        
        overlap = t1 & t2
        print(t1)
        print(t2)
        if (JsonNumeric.NAMES & t1) and (JsonNumeric.NAMES & t2) and (not t1 & t2):
            overlap.add(JsonNumeric.NAME)

        print("lhs: ", s1)
        print("rhs: ", s2)
        print("overlap: ", overlap)
        if not overlap:
            return True
        else:
            from checkers import JSON_SUBTYPE_CHECKERS
            results = []
            for t in overlap:
                results.append(JSON_SUBTYPE_CHECKERS.get(t)(s1, s2))
            if all(results):
                return True
            else: 
                return False

                
        # numeric = ["number", "integer"]
        # if t1 in numeric and t2 in numeric:
        #     ret = checkers.is_numeric_subtype(s1, s2)

        # if (t1 == t2 == "string"):
        #     ret = checkers.is_string_subtype(s1, s2)

        # if (t1 == t2 == "array"):
        #     ret = checkers.is_array_subtype(s1, s2)

        # return ret


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
