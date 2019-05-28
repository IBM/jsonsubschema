'''
Created on May 20, 2019
@author: Andrew Habib
'''

import intervals as I
from SubTypeChecker import SubTypeChecker
from Utils import PythonTypes

is_num = PythonTypes.is_num


class JsonNumber:

    def __init__(self, s):
        #
        self.min = s.get("minimum")
        self.xmin = s.get("exclusiveMinimum")
        self.max = s.get("maximum")
        self.xmax = s.get("exclusiveMaximum")
        self.mulOf = s.get("multipleOf")

    def get_interval_draf4(self):
        #
        _min = self.min
        _xmin = self.xmin
        _max = self.max
        _xmax = self.xmax
        #
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
        #
        return i


def is_subtype(s1, s2):
    s1 = JsonNumber(s1)
    s2 = JsonNumber(s2)
    #
    is_sub_interval = s1.get_interval_draf4() in s2.get_interval_draf4()
    if is_sub_interval and \
            (
                (not is_num(s1.mulOf) and not is_num(s2.mulOf))
            or (is_num(s1.mulOf) and not is_num(s2.mulOf))
            or (is_num(s1.mulOf) and is_num(s2.mulOf) and s1.mulOf % s2.mulOf == 0)
            ):
        return True
    return False
