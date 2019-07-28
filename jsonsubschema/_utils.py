'''
Created on May 24, 2019
@author: Andrew Habib
'''


import copy
import math
import numbers

import fractions as frac

import jsonschema
import intervals as I
from greenery.lego import parse

import jsonsubschema.config as config


def is_str(i):
    return isinstance(i, str)


def is_int(i):
    if isinstance(i, bool):
        return False
    return isinstance(i, int)


def is_int_equiv(i):
    if isinstance(i, bool):
        return False
    return isinstance(i, int) or (isinstance(i, float) and float(i).is_integer())


def is_float(i):
    return isinstance(i, float)


def is_num(i):
    if isinstance(i, bool):
        return False
    return isinstance(i, numbers.Number)


def is_bool(i):
    return isinstance(i, bool)


def is_null(i):
    isinstance(i, type(None))


def is_list(i):
    return isinstance(i, list)


def is_dict(i):
    return isinstance(i, dict)


def is_empty_dict_or_none(i):
    return i == {} or i == None


def is_dict_or_true(i):
    return isinstance(i, dict) or i == True


def validate_schema(s):
    return config.VALIDATOR.check_schema(s)


def get_valid_enum_vals(enum, s):
    # copy eum into set for two reasons:
    # 1- we need to modify a different copy from what we iterate on
    # 2- hashing elements into set and back to list will guarantee
    # the list is ordered and hence JSONschema __eq__ with enums should work.
    vals = set(enum)
    for i in enum:
        try:
            jsonschema.validate(instance=i, schema=s)
        except jsonschema.ValidationError:
            vals.remove(i)
    return list(vals)


def print_db(*args, **kwargs):
    if config.PRINT_DB:
        print("".join(str(arg) + " " for arg in args))


def one(iterable):
    for i in range(len(iterable)):
        if iterable[i]:
            return not (any(iterable[:i]) or any(iterable[i+1:]))
    return False


def regex_unanchor(p):
    # We need this cuz JSON regexs are not anchored by default
    # while the regex library we use assumes the opposite:
    # regexes are anchored by default AND ^ and $ are literals
    # and don't carry their anchoring meaning.
    if p:
        if p[0] == "^":
            p = p[1:]
        else:
            p = ".*" + p
        if p[-1] == "$":
            p = p[:-1]
        else:
            p = p + ".*"
    return p

def regex_matches_string(regex=None, s=None):
    return parse(regex).matches(s)

def regex_meet(s1, s2, *args):
    ret = parse(s1) & parse(s2)
    for arg in args:
        ret = ret & parse(arg)
    return str(ret) if not ret.empty() else None


def regex_isSubset(s1, s2):
    ''' regex subset is quite expensive to compute
        especially for complex patterns. '''
    return (parse(s1) & parse(s2).everythingbut()).empty()

def regex_isProperSubset(s1, s2):
    ''' regex proper subset is quite expensive to compute
        so we try to break it into two separate checks,
        and do the more expensive check, only if the 
        cheaper one passes first.'''
    if not parse(s1).equivalent(parse(s2)):
        if regex_isSubset(s1, s2):
            return True
    return False

def complement_of_string_pattern(s):
    return str(parse(s).everythingbut())


def lcm(x, y):
    bad_values = [I.inf, -I.inf, None]
    if x in bad_values:
        if y in bad_values:
            return None
        else:
            return y
    elif y in bad_values:
        return x
    else:
        if is_int(x) and is_int(y):
            return x * y / math.gcd(int(x), int(y))
        else:
            # import warnings
            # with warnings.catch_warnings():
            #     warnings.filterwarnings("ignore", category=DeprecationWarning)
            return x * y / frac.gcd(x, y)
