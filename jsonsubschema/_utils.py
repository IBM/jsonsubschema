'''
Created on May 24, 2019
@author: Andrew Habib
'''

import numbers

import config

import intervals as I

schema_validator = config.VALIDATOR


def validate_schema(s):
    return schema_validator.check_schema(s)


def print_db(*args, **kwargs):
    if config.PRINT_DB:
        print("".join(str(arg) + " " for arg in args))


def one(iterable):
    for i in range(len(iterable)):
        if iterable[i]:
            print(i, iterable[i])
            return not (any(iterable[:i]) or any(iterable[i+1:]))
    return False


class PythonTypes:

    @staticmethod
    def is_num(i):
        return isinstance(i, int) or isinstance(i, numbers.Number)

    @staticmethod
    def is_str(i):
        return isinstance(i, str)

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
is_list = PythonTypes.is_list
is_dict = PythonTypes.is_dict
is_empty_dict_or_none = PythonTypes.is_empty_dict_or_none
is_dict_or_true = PythonTypes.is_dict_or_true


def get_interval_from_optional_min_max(min=None, max=None):
    if is_num(min):
        if is_num(max):
            i = I.closed(min, max)
        else:
            i = I.closed(min, I.inf)
    else:
        if is_num(max):
            i = I.closed(-I.inf, max)
        else:
            i = I.closed(-I.inf, I.inf)
    return i


def is_sub_interval_from_optional_ranges(min1=None, max1=None, min2=None, max2=None):
    i1 = get_interval_from_optional_min_max(min1, max1)
    i2 = get_interval_from_optional_min_max(min2, max2)
    if i1 and i2:
        return i1 in i2
    else:
        return True


def handle_uninhabited_types(s1, s2):
    if s2.isUninhabited:
        if s1.isUninhabited:
            # False <: False
            print_db("Uninhabited type: __11__")
            return True
        else:
            # !False <: False
            print_db("Uninhabited type: __01__")
            return False
    else:
        if s1.isUninhabited:
            # False <: !False
            print_db("Uninhabited type: __10__")
            return True
    # !False <: !False
    # print_db("are_inhibited_types: __00__")


def get_types_or_implicit_types(s):
    types = type_to_list(s)
    # type has higher precedence over keywords
    if types:
        return types
    kw_to_type = json_keywords_to_types()
    types = set(types)
    for k in s.keys():
        # skip adding 'number' to types
        # if 'integer' is already in.
        from _types import JsonNumeric
        if k in JsonNumeric.KEY_WORDS and "integer" in types:
            continue
        #
        t = kw_to_type.get(k)
        if t:
            types.add(t)
    types = list(types)
    return types


def type_to_list(s):
    t = s.get("type", [])
    if isinstance(t, str):
        return [t]
    else:
        return t


def json_keywords_to_types():
    kw_to_type = {}
    from _types import JSON_TYPES
    for json_type in JSON_TYPES:
        for kw in json_type.KEY_WORDS:
            kw_to_type[kw] = json_type.NAME
    return kw_to_type
