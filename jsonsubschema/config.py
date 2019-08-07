'''
Created on June 24, 2019
@author: Andrew Habib
'''

import sys
import jsonschema

this = sys.modules[__name__]

# Change here which schema validator to use
this.VALIDATOR = jsonschema.Draft4Validator


def set_json_validator_version(v=jsonschema.Draft4Validator):
    ''' Currently, our subtype checking supports json schema draft 4 only,
        so VALIDATOR should not changed.
        We prodive the method for future support of other json schema versions. '''

    this.VALIDATOR = v


# Print debugging info?
this.PRINT_DB = False


def set_debug(b=False):
    if b:
        this.PRINT_DB = True
    else:
        this.PRINT_DB = False


# Enable uninhabited types warning?
this.WARN_UNINHABITED = False


def set_warn_uninhabited(b=False):
    if b:
        this.WARN_UNINHABITED = True
    else:
        this.WARN_UNINHABITED = False
