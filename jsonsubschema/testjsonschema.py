'''
Created on June 24, 2019
@author: Andrew Habib
'''

import json
import sys

from jsonsubschema.checker import (
    JSONSubSchemaFactory,
    isSubschema
)

if __name__ == "__main__":

    s1_file = sys.argv[1]
    s2_file = sys.argv[2]
    print("Loading json schemas from:\n{}\n{}\n".format(s1_file, s2_file))

    #######################################

    # with open(s1_file, 'r') as f1:
    #     s1 = json.load(f1, cls=JSONSubSchemaFactory)
    # with open(s2_file, 'r') as f2:
    #     s2 = json.load(f2, cls=JSONSubSchemaFactory)
    # print(s1)
    # print(s2)
    # print("Usage scenario 1:", s1.isSubtype(s2))

    #######################################

    with open(s1_file, 'r') as f1:
        s1 = json.load(f1)
    with open(s2_file, 'r') as f2:
        s2 = json.load(f2)
    
    print()
    print("LHS <: RHS", isSubschema(s1, s2))
    print()
    print("RHS <: LHS", isSubschema(s2, s1))