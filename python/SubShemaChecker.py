'''
Created on May 17, 2019
@author: Andrew Habib
'''

import json
import jsonschema
import sys

import NumberSubTypeChecker
import StringSubTypeChecker
import ArraySubTypeChecker


class SubSchemaChecker(object):
    # Change here which validator to use.
    VALIDATOR = jsonschema.Draft3Validator

    '''
    The checker class constructor accepts two 'valid' json files.
    '''

    def __init__(self, s1=None, s2=None):
        self.s1 = s1
        self.s2 = s2
        if self.s1 and self.s2:
            self.validate_schemas()

    def validate_schemas(self):
        '''
        Validate given schemas against the pre-defined VALIDATOR schema.
        '''
        def err(s, e):
            print("Error while validating input schema:\n{}".format(s))
            print("Json path:: {}".format(e.path))
            print("Msg: {}".format(e.message))
            sys.exit(1)

        try:
            self.VALIDATOR.check_schema(self.s1)
        except jsonschema.exceptions.SchemaError as e:
            err(s1, e)

        try:
            self.VALIDATOR.check_schema(self.s2)
        except jsonschema.exceptions.SchemaError as e:
            err(s2, e)

    @staticmethod
    def is_sub_schema(s1, s2):
        '''
        Is s1 <: s2 ?
        '''
        # print("Is")
        # print(s1)
        # print("subschema of")
        # print(s2)
        # print()

        # Trivial cases:
        # should have more general procedures for these?
        if s2 is True or not s2:
            return True
        if s2 is False or ("not" in s2.keys() and not s2["not"]):
            return False

        # Real stuff
        t1 = s1.get("type")
        t2 = s2.get("type")
        if s1 == s2:
            print(
                "Warning: any schema is sub-schema of itself. This will always be true.")
            print("Caution: Inhibited types are NOT checked.")
            return True

        ret = False
        if (t1 == t2 == "integer") or (t1 == t2 == "number") or (t1 == "integer" and t2 == "number"):
            ret = NumberSubTypeChecker.is_subtype(s1, s2)
        if (t1 == t2 == "string"):
            ret = StringSubTypeChecker.is_subtype(s1, s2)
        if (t1 == t2 == "array"):
            ret = ArraySubTypeChecker.is_subtype(s1, s2)
        return ret


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

    checker = SubSchemaChecker(s1, s2)
    print(checker.is_sub_schema(s1, s2))
