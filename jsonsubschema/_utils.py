'''
Created on May 24, 2019
@author: Andrew Habib
'''


import copy
import math
import numbers
import re
import jsonschema
import fractions as frac
import intervals as I
from greenery.lego import parse

import jsonsubschema.config as config
import jsonsubschema._constants as definitions


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


# def is_float(i):
#     return isinstance(i, float)


def is_num(i):
    if isinstance(i, bool):
        return False
    return isinstance(i, numbers.Number)


def is_bool(i):
    return isinstance(i, bool)


# def is_null(i):
#     isinstance(i, type(None))


def is_list(i):
    return isinstance(i, list)


def is_dict(i):
    return isinstance(i, dict)


# def is_empty_dict_or_none(i):
#     return i == {} or i == None


# def is_dict_or_true(i):
#     return isinstance(i, dict) or i == True


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
    try:
        return sorted(vals)
    except TypeError:
        return list(vals)


def get_typed_enum_vals(enum, t):
    if t is "integer":
        enum = filter(lambda i: not isinstance(i, bool), enum)
    return sorted(filter(lambda i: isinstance(i, definitions.JtypesToPyTypes[t]), enum))


def print_db(*args):
    if config.PRINT_DB:
        if args:
            print("".join(str(arg) + " " for arg in args))
        else:
            print()


# def one(iterable):
#     for i in range(len(iterable)):
#         if iterable[i]:
#             return not (any(iterable[:i]) or any(iterable[i+1:]))
#     return False

#
# To avoid regex bottlenecks, instead of using '.*'
# as the default value for string.pattern, we use
# 'None' and apply explicit checks for 'None'.
# E.g. regex_meet(s1, None) = s1
#


def prepare_pattern_for_greenry(s):
    ''' The greenery library we use for regex intersection assumes 
        patterns are unanchored by default. Anchoring chars ^ and $ are
        treated as literals by greenery.
        So basically strip any non-escaped ^ and $ when using greenery.
        Moreover, for any escaped ^ or $, we remove the \ to adhere to 
        greenery syntax (when they are escaped, they are literals). '''

    s = re.sub(r'(?<!\\|\[)((?:\\{2})*)\^', r'\g<1>',
               s)  # strip non-escaped ^ that is not inside []
    s = re.sub(r'(?<!\\)((?:\\{2})*)\$', r'\g<1>', s)  # strip non-escaped $
    s = re.sub(r'(?<!\\)((?:\\{1})*)\\\^', r'\g<1>^', s)  # strip \ before ^
    s = re.sub(r'(?<!\\)((?:\\{1})*)\\\$', r'\g<1>$', s)  # strip \ before $

    return s


def regex_unanchor(p):
    # We need this cuz JSON regexs are not anchored by default
    # while the regex library we use assumes the opposite:
    # regexes are anchored by default AND ^ and $ are literals
    # and don't carry their anchoring meaning.
    if p:
        if p[0] == "^":
            p = p[1:]
        elif p[:2] != ".*":
            p = ".*" + p
        if p[-1] == "$":
            p = p[:-1]
        elif p[-2:] != ".*":
            p = p + ".*"
    # else:  # case p == "" the empty string
    #     p = ".*"
    return p


def regex_matches_string(regex=None, s=None):
    if regex:
        return parse(regex).matches(s)
    else:
        return True


def regex_meet(s1, s2):
    if s1 and s2:
        ret = parse(s1) & parse(s2)
        return str(ret.reduce()) if not ret.empty() else None
    elif s1:
        return s1
    elif s2:
        return s2
    else:
        return None


def regex_isSubset(s1, s2):
    ''' regex subset is quite expensive to compute
        especially for complex patterns. '''
    if s1 and s2:
        s1 = parse(s1).reduce()
        s2 = parse(s2).reduce()
        return s1.equivalent(s2) or (s1 & s2.everythingbut()).empty()
    elif s1:
        return True
    elif s2:
        return False


# def regex_isProperSubset(s1, s2):
#     ''' regex proper subset is quite expensive to compute
#         so we try to break it into two separate checks,
#         and do the more expensive check, only if the
#         cheaper one passes first. '''

#     s1 = parse(s1).reduce()
#     s2 = parse(s2).reduce()
#     if not s1.equivalent(s2):
#         return (s1 & s2.everythingbut()).empty()
#     return False


def string_range_to_regex(min, max):
    assert min <= max, ""
    if min == max:
        pattern = ".{" + str(min) + "}"             # '.{min}'
    elif max == I.inf:
        pattern = ".{" + str(min) + ",}"            # '.{min,}'
    else:
        pattern = ".{" + str(min) + "," + str(max) + "}"  # '.{min, max}'

    return pattern


def complement_of_string_pattern(s):
    return str(parse(s).everythingbut().reduce())


def lcm(x, y):
    bad_values = [None, ]#I.inf, -I.inf]
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

def gcd(x, y):
    bad_values = [None, ]#I.inf, -I.inf, None]
    if x in bad_values:
        if y in bad_values:
            return None
        else:
            return None
    elif y in bad_values:
        return None
    else:
        if is_int(x) and is_int(y):
            return math.gcd(int(x), int(y))
        else:
            # import warnings
            # with warnings.catch_warnings():
            #     warnings.filterwarnings("ignore", category=DeprecationWarning)
            return frac.gcd(x, y)
