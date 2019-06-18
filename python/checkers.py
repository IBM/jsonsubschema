'''
Created on May 20, 2019
@author: Andrew Habib
'''

import sys
import math

import intervals as I

from greenery.lego import parse

import subschemachecker

from _types import (
    JsonString,
    JsonNumeric,
    JsonArray,
    JsonObject
)
from _utils import (
    print_db,
    is_sub_interval_from_optional_ranges,
    is_num,
    is_list,
    is_dict,
    is_empty_dict_or_none,
    is_dict_or_true
)


def is_string_subtype(s1, s2):
    if s2.get("type") != "string":
        return False
    #
    s1 = JsonString(s1)
    s2 = JsonString(s2)
    #
    # uninhabited = handle_uninhabited_types(s1, s2)
    # if uninhabited != None:
    #     return uninhabited
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


def is_numeric_subtype(s1, s2):
    if s2.get("type") not in ["integer", "number"]:
        return False
    #
    s1 = JsonNumeric.get_proper_JsonNumeric(s1)
    s2 = JsonNumeric.get_proper_JsonNumeric(s2)
    print_db(s1)
    print_db(s1.type)
    print_db(s2)
    print_db(s2.type)
    #
    # unInhabited = handle_uninhabited_types(s1, s2)
    # if unInhabited != None:
    #     return unInhabited
    #
    is_sub_interval = s1.interval in s2.interval
    if not is_sub_interval:
        print_db("num__00")
        return False
    #
    if s1.type == "number" and s2.type == "integer":
        print_db("num__01")
        return False
    #
    if (s1.mulOf == s2.mulOf) \
            or (s1.mulOf != None and s2.mulOf == None) \
            or (s1.mulOf != None and s2.mulOf != None and s1.mulOf % s2.mulOf == 0) \
            or (s1.mulOf == None and s2.mulOf == 1):
        print_db("num__02")
        return True


def is_array_subtype(s1, s2):
    if s2.get("type") != "array":
        return False
    #
    #
    s1 = JsonArray(s1)
    s2 = JsonArray(s2)
    #
    # uninhabited = handle_uninhabited_types(s1, s2)
    # if uninhabited != None:
    #     return uninhabited
    #
    # -- minItems and maxItems
    is_sub_interval = is_sub_interval_from_optional_ranges(
        s1.min, s1.max, s2.min, s2.max)
    # also takes care of {'items' = [..], 'addItems' = False}
    if not is_sub_interval:
        print_db("__01__")
        return False
    #
    # -- unique
    # TODO Double-check. Could be more subtle?
    if not s1.uniq and s2.uniq:
        print_db("__02__")
        return False
    #
    # -- items = {not empty}
    # no need to check addItems
    if is_dict(s1.items):
        if is_dict(s2.items):
            if subschemachecker.Checker.is_subtype(s1.items, s2.items):
                print_db("__05__")
                return True
            else:
                print_db("__06__")
                return False
        elif is_list(s2.items):
            if s2.addItems == False:
                print_db("__07__")
                return False
            elif s2.addItems == True:
                for i in s2.items:
                    if not subschemachecker.Checker.is_subtype(s1.items, i):
                        print_db("__08__")
                        return False
                print_db("__09__")
                return True
            elif is_dict(s2.addItems):
                for i in s2.items:
                    if not subschemachecker.Checker.is_subtype(s1.items, i):
                        print_db("__10__")
                        return False
                if subschemachecker.Checker.is_subtype(s1.items, s2.addItems):
                    print_db("__11__")
                    return True
                else:
                    print_db("__12__")
                    return False
    #
    elif is_list(s1.items):
        if is_dict(s2.items):
            if s1.addItems == False:
                for i in s1.items:
                    if not subschemachecker.Checker.is_subtype(i, s2.items):
                        print_db("__13__")
                        return False
                print_db("__14__")
                return True
            elif s1.addItems == True:
                for i in s1.items:
                    if not subschemachecker.Checker.is_subtype(i, s2.items):
                        return False
                return True
            elif is_dict(s1.addItems):
                for i in s1.items:
                    if not subschemachecker.Checker.is_subtype(i, s2.items):
                        return False
                if subschemachecker.Checker.is_subtype(s1.addItems, s2.items):
                    return True
                else:
                    return False
        # now lhs and rhs are lists
        elif is_list(s2.items):
            len1 = len(s1.items)
            len2 = len(s2.items)
            for i, j in zip(s1.items, s2.items):
                if not subschemachecker.Checker.is_subtype(i, j):
                    return False
            if len1 == len2:
                if s1.addItems == s2.addItems:
                    return True
                elif s1.addItems == True and s2.addItems == False:
                    return False
                elif s1.addItems == False and s2.addItems == True:
                    return True
                else:
                    return subschemachecker.Checker.is_subtype(s1.addItems, s2.addItems)
            elif len1 > len2:
                diff = len1 - len2
                for i in range(len1-diff, len1):
                    if not subschemachecker.Checker.is_subtype(s1.items[i], s2.addItems):
                        print_db("9999")
                        return False
                print_db("8888")
                return True
            else:  # len2 > len 1
                # if s1.addItems:
                diff = len2 - len1
                for i in range(len2 - diff, len2):
                    print_db("s1.addItems", s1.addItems)
                    print_db(i, s2.items[i])
                    if not subschemachecker.Checker.is_subtype(s1.addItems, s2.items[i]):
                        print_db("!!!")
                        return False
                return subschemachecker.Checker.is_subtype(s1.addItems, s2.addItems)


def is_object_subtype(s1, s2):
    if s2.get("type") != "object":
        return False


def is_anyof_subtype(s1, s2):

    s1 = s1.get("anyOf")

    import subschemachecker
    for s in s1:
        if not subschemachecker.Checker.is_subtype(s, s2):
            return False
    return True


def is_anyof_subtype_rhs(s1, s2):

    s2 = s2.get("anyOf")

    import subschemachecker
    for s in s2:
        if subschemachecker.Checker.is_subtype(s1, s):
            return True
    return False


def is_allof_subtype(s1, s2):

    s1_list = s1.get("allOf") or [s1]
    s2_list = s2.get("allOf") or [s2]

    for s in s1_list:
        if not has_supertype_in_list(s, s2_list):
            return False
    return True


def has_supertype_in_list(s, s_list):
    for s_ in s_list:
        if subschemachecker.Checker.is_subtype(s, s_):
            return True
    return False


JSON_SUBTYPE_CHECKERS = {
    "string": is_string_subtype,
    "number": is_numeric_subtype,
    "integer": is_numeric_subtype,
    "array": is_array_subtype,
    "object": is_object_subtype,
    "anyOf": is_anyof_subtype,
    "anyOf_rhs": is_anyof_subtype_rhs
}
