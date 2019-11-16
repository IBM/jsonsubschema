'''
Created on June 24, 2019
@author: Andrew Habib
'''

import sys

from jsonsubschema._utils import load_json_file
from jsonsubschema.api import isSubschema


def main():

    assert len(
        sys.argv) == 3, "jsonsubschema cli takes exactly two arguments lhs_schema and rhs_schema"

    s1_file = sys.argv[1]
    s2_file = sys.argv[2]

    s1 = load_json_file(s1_file, "LHS file:")
    s2 = load_json_file(s2_file, "RHS file:")

    print("LHS <: RHS", isSubschema(s1, s2))
    print("RHS <: LHS", isSubschema(s2, s1))


if __name__ == "__main__":

    main()
