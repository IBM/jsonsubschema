'''
Created on May 24, 2019
@author: Andrew Habib
'''

import intervals as I
from SubTypeChecker import SubTypeChecker, Python_Types

is_num = Python_Types.is_num


def get_interval_from_json_number_draf4(s):
    _min = s.get("minimum")
    _xmin = s.get("exclusiveMinimum")
    _max = s.get("maximum")
    _xmax = s.get("exclusiveMaximum")

    if is_num(_min) and is_num(_max):
        if _xmin and _xmax:
            i = I.open(_min, _max)
        elif _xmin and not _xmax:
            i = I.openclosed(_min, _max)
        elif not _xmin and _xmax:
            i = I.closedopen(_min, _max)
        else:
            i = I.closed(_min, _max)
    elif is_num(_min) and not is_num(_max):
        if _xmin:
            i = I.open(_min, I.inf)
        else:
            i = I.closed(_min, I.inf)
    elif not is_num(_min) and is_num(_max):
        if _xmax:
            i = I.open(-I.inf, _max)
        else:
            i = I.closed(-I.inf, _max)
    elif not is_num(_min) and not is_num(_max):
        i = I.closed(-I.inf, I.inf)

    return i


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
