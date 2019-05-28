'''
Created on May 24, 2019
@author: Andrew Habib
'''

import intervals as I
from greenery.lego import parse
from SubTypeChecker import SubTypeChecker
from Utils import is_sub_interval_from_optional_ranges


class JsonString:

    def __init__(self, s):
        #
        self.min = s.get("minLength")
        self.max = s.get("maxLength")
        self.pattern = s.get("pattern")


def is_subtype(s1, s2):
    #
    s1 = JsonString(s1)
    s2 = JsonString(s2)
    #
    is_sub_interval = is_sub_interval_from_optional_ranges(
        s1.min, s1.max, s2.min, s2.max)
    if not is_sub_interval:
        return False
    #
    # at this point, length is compatible,
    # so we should now worry about pattern only.
    if s1.pattern == None or s2.pattern == "":
        return True
    elif s1.pattern == None or s1.pattern == "":
        return False
    else:
        regex1 = parse(s1.pattern)
        regex2 = parse(s2.pattern)
        result = regex1 & regex2.everythingbut()
        if result.empty():
            return True
        else:
            return False
