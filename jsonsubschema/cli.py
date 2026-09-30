'''
Created on June 24, 2019
@author: Andrew Habib
'''

import argparse

from jsonsubschema._utils import load_json_file
from jsonsubschema.api import isSubschema, schemaDiff


def main():
    ''' CLI entry point for jsonsubschema '''

    parser = argparse.ArgumentParser(description='CLI for jsonsubschema tool which checks whether a LHS JSON schema is a subschema (<:) of another RHS JSON schema.')
    parser.add_argument('LHS', metavar='lhs', type=str, help='Path to the JSON file which has the LHS JSON schema')
    parser.add_argument('RHS', metavar='rhs', type=str, help='Path to the JSON file which has the RHS JSON schema')
    parser.add_argument('--diff', action='store_true',
                        help='Show compatibility relationship instead of subtype check')

    args = parser.parse_args()
    s1_file_path = args.LHS
    s2_file_path = args.RHS

    s1 = load_json_file(s1_file_path, "LHS file:")
    s2 = load_json_file(s2_file_path, "RHS file:")

    if args.diff:
        print("Compatibility:", schemaDiff(s1, s2))
    else:
        print("LHS <: RHS", isSubschema(s1, s2))

if __name__ == "__main__":

    main()
