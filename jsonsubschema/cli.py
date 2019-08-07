'''
Created on June 24, 2019
@author: Andrew Habib
'''

import json
import sys

from jsonsubschema.api import isSubschema


def main():

    assert len(
        sys.argv) == 3, "jsonsubschema cli takes exactly two arguments lhs_schema and rhs_schema"

    s1_file = sys.argv[1]
    s2_file = sys.argv[2]

    with open(s1_file, 'r') as f1:
        s1 = json.load(f1)
    with open(s2_file, 'r') as f2:
        s2 = json.load(f2)

    print("LHS <: RHS", isSubschema(s1, s2))
    print("RHS <: LHS", isSubschema(s2, s1))


if __name__ == "__main__":

    main()
