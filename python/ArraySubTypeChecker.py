'''
Created on May 25, 2019
@author: Andrew Habib
'''

import intervals as I

from JsonType import JsonType
from Utils import PythonTypes, is_sub_interval_from_optional_ranges, print_db, handle_uninhabited_types

is_dict_or_none = PythonTypes.is_dict_or_none
is_dict_or_true = PythonTypes.is_dict_or_true
is_list = PythonTypes.is_list
is_num = PythonTypes.is_num


class JsonArray(JsonType):

    def __init__(self, s):
        #
        self.items = s.get("items")
        self._min = s.get("minItems")
        self._max = s.get("maxItems")
        self.uniq = s.get("uniqueItems")
        self.addItems = s.get("additionalItems")
        #
        self.compute_actual_min()
        self.compute_actual_max()
        #
        super().__init__()

    def compute_actual_min(self):
        #
        if not is_num(self._min):
            self.min = 0
        # elif is_list(self.items) and self.addItems == False:
        #     length = len(self.items)
        #     if self._min > length:
        #         # This is equivalence to False schema! Nothing validates against this.
        #         # How to replace this schema with False, and continue the checking
        #         # so that this is subtype of anything,
        #         # and nothing is subtype of it.
        #         print("WARNING: Array minItems = {} while it can't accept more than {} items.".format(
        #             self._min, length))
        #         print("This schema will accept no array at all.")
        #         print("Should terminate sub-schema checking here!?")
        #     else:  # aka, self._min <= length
        #         self.min = self._min
        # else:
        #     self.min = self._min
        else:
            self.min = self._min

    def compute_actual_max(self):
        #
        if is_num(self._max):
            if is_list(self.items) and self.addItems == False:
                length = len(self.items)
                self.max = min(self._max, length)
            else:
                self.max = self._max
        else:
            if is_list(self.items) and self.addItems == False:
                length = len(self.items)
                self.max = length
            else:
                self.max = I.inf

    def check_uninhabited(self):
        if (is_list(self.items) and self.addItems == False
            and is_num(self._min) and self._min > len(self.items)) \
           or (self.min > self.max):
            self.isInhibited = True


def is_subtype(s1, s2):
    #
    s1 = JsonArray(s1)
    s2 = JsonArray(s2)
    #
    uninhabited = handle_uninhabited_types(s1, s2)
    if uninhabited != None:
        return uninhabited
    #
    is_sub_interval = is_sub_interval_from_optional_ranges(
        s1.min, s1.max, s2.min, s2.max)
    #
    # I) Easy true cases
    # case length compatible AND super- allows anything
    if is_sub_interval and \
            (is_dict_or_none(s2.items) or is_dict_or_true(s2.addItems)):
        print_db("__01__")
        return True
    #
    # II) Easy false cases:
    # case incompatible length
    if not is_sub_interval:
        print_db("__02__")
        return False
    # case sub- is not unique and super- is
    if not s1.uniq and s2.uniq:
        print_db("__03__")
        return False
    # case sub- allows anything but super- does not
    if (is_dict_or_none(s1.items) or is_dict_or_true(s1.addItems)) and \
            not (is_dict_or_none(s2.items) or is_dict_or_true(s2.addItems)):
        print_db("__04__")
        return False
    #
    # III) Nasty false cases
    # case super- has restrictions and sub- does not
    if is_list(s2.items) and is_list(s1.items):
        if not is_dict_or_true(s2.addItems) \
                and not is_sub_interval:
            # and (len(s1.items) > len(s2.items)
            #      or (is_num(s2.max) and len(s1.items) > s2.max)
            #      ):
            # and (not is_num(s1.max) or ):
            print_db("__05__")
            return False
        elif len(s1.items) <= len(s2.items):
            from SubShemaChecker import SubSchemaChecker
            for t1, t2 in zip(s1.items, s2.items):
                c = SubSchemaChecker()
                if not c.is_sub_schema(t1, t2):
                    print_db("__06__")
                    return False
            # All cases, that I can think of, have been checked.
            # So if we reach here, then probably we should return True!
            print_db("__07__")
            return True
