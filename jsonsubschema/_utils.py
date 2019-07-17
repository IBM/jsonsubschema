'''
Created on May 24, 2019
@author: Andrew Habib
'''


import math
import numbers

import fractions as frac

import intervals as I
from greenery.lego import parse

import config

schema_validator = config.VALIDATOR


def validate_schema(s):
    return schema_validator.check_schema(s)


def print_db(*args, **kwargs):
    if config.PRINT_DB:
        print("".join(str(arg) + " " for arg in args))


def regex_meet(s1, s2, *args):
    ret = parse(s1) & parse(s2)
    for arg in args:
        ret = ret & parse(arg)
    return str(ret) if not ret.empty() else None


def regex_isSubset(s1, s2):
    return (parse(s1) & parse(s2).everythingbut()).empty()


def lcm(x, y):
    if x == I.inf or x == -I.inf or x == None:
        if y == I.inf or y == -I.inf or y == None:
            return None
        else:
            return y
    elif y == I.inf or y == -I.inf or y == None:
        return x
    else:
        return x * y / frac.gcd(x, y)


def one(iterable):
    for i in range(len(iterable)):
        if iterable[i]:
            return not (any(iterable[:i]) or any(iterable[i+1:]))
    return False


class PythonTypes:

    @staticmethod
    def is_str(i):
        return isinstance(i, str)

    @staticmethod
    def is_num(i):
        return isinstance(i, int) or isinstance(i, numbers.Number)

    @staticmethod
    def is_bool(i):
        return isinstance(i, bool)

    @staticmethod
    def is_list(i):
        return isinstance(i, list)

    @staticmethod
    def is_dict(i):
        return isinstance(i, dict)

    @staticmethod
    def is_empty_dict_or_none(i):
        return i == {} or i == None

    @staticmethod
    def is_dict_or_true(i):
        return isinstance(i, dict) or i == True


is_num = PythonTypes.is_num
is_bool = PythonTypes.is_bool
is_list = PythonTypes.is_list
is_dict = PythonTypes.is_dict
is_empty_dict_or_none = PythonTypes.is_empty_dict_or_none
is_dict_or_true = PythonTypes.is_dict_or_true
