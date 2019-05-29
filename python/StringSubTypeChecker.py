'''
Created on May 24, 2019
@author: Andrew Habib
'''

import intervals as I

from greenery.lego import parse
from JsonType import JsonType
from Utils import is_sub_interval_from_optional_ranges, handle_uninhabited_types


class JsonString(JsonType):

    def __init__(self, s):
        self.min = s.get("minLength")
        self.max = s.get("maxLength")
        self.pattern = s.get("pattern")
        #
        super().__init__()

    def check_uninhabited(self):
        if self.min > self.max:
            self.isInhibited = True
        # TODO
        # missing cases where min/max length might be
        # not compatible with pattern?


def is_subtype(s1, s2):
    #
    s1 = JsonString(s1)
    s2 = JsonString(s2)
    #
    uninhabited = handle_uninhabited_types(s1, s2)
    if uninhabited != None:
        return uninhabited
    #
    is_sub_interval = is_sub_interval_from_optional_ranges(
        s1.min, s1.max, s2.min, s2.max)
    if not is_sub_interval:
        return False
    #
    # at this point, length is compatible,
    # so we should now worry about pattern only.
    if s2.pattern == None or s2.pattern == "":
        return True
    elif s1.pattern == None or s1.pattern == "":
        return False
    elif s1.pattern == s2.pattern:
        return True
    else:
        regex1 = parse(s1.pattern)
        regex2 = parse(s2.pattern)
        result = regex1 & regex2.everythingbut()
        if result.empty():
            return True
        else:
            return False
