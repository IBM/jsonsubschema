'''
Created on May 24, 2019
@author: Andrew Habib
'''

import numbers

import intervals as I


PRINT_DB = True


def print_db(s=None):
    if PRINT_DB:
        print(s)


class PythonTypes:
    @staticmethod
    def is_num(i):
        return isinstance(i, int) or isinstance(i, numbers.Number)

    @staticmethod
    def is_str(i):
        return isinstance(i, str)

    @staticmethod
    def is_dict_or_none(i):
        return isinstance(i, dict) or i == None

    @staticmethod
    def is_dict_or_true(i):
        return isinstance(i, dict) or i == True

    @staticmethod
    def is_list(i):
        return isinstance(i, list)


is_num = PythonTypes.is_num


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
    if s2.isInhibited:
        if s1.isInhibited:
            # False <: False
            print_db("are_inhibited_types: __11__")
            return True
        else:
            # !False <: False
            print_db("are_inhibited_types: __01__")
            return False
    else:
        if s1.isInhibited:
            # False <: !False
            print_db("are_inhibited_types: __10__")
            return True
    # !False <: !False
    print_db("are_inhibited_types: __00__")
