'''
Created on May 25, 2019
@author: Andrew Habib
'''

import intervals as I
# from SubShemaChecker import SubSchemaChecker
from SubTypeChecker import SubTypeChecker
from Utils import Python_Types, is_sub_interval_from_optional_ranges

is_dict_or_none = Python_Types.is_dict_or_none
is_dict_or_true = Python_Types.is_dict_or_true
is_list = Python_Types.is_list
is_num = Python_Types.is_num


class ArraySubTypeChecker(SubTypeChecker):

    def is_subtype(self):
        s1 = self.s1
        s2 = self.s2
        #
        min1 = s1.get("minItems")
        max1 = s1.get("maxItems")
        uniq1 = s1.get("uniqueItems")
        items1 = s1.get("items")
        addItems1 = s1.get("additionalItems")
        #
        min2 = s2.get("minItems")
        max2 = s2.get("maxItems")
        uniq2 = s2.get("uniqueItems")
        items2 = s2.get("items")
        addItems2 = s2.get("additionalItems")
        # I) Easy false cases:
        # case incompatible length
        is_sub_interval = is_sub_interval_from_optional_ranges(
            min1, max1, min2, max2)
        if not is_sub_interval:
            return False
        # case sub- is not unique and super- is
        if not uniq1 and uniq2:
            return False
        # case sub- allows anything but super- does not
        if (is_dict_or_none(items1) or is_dict_or_true(addItems1)) and \
            not (is_dict_or_none(items2) or is_dict_or_true(addItems2)):
            return False
        # case super- has restrictions and sub- does not
        if is_list(items2) and is_list(items1):
            if not is_dict_or_true(addItems2) \
                and (len(items1) > len(items2) \
                    or (is_num(max2) and len(items1) > max2)
                ):
                return False
            # elif len(items1) == len(items2):
                # from SubShemaChecker import SubSchemaChecker
                # for t1, t2 in zip(items1, items2):
                #     print(t1)
                #     print(t2)
                #     c = SubSchemaChecker(t1, t2)
                #     if not c.is_sub_schema():
                #         return False
                return True
        # II) Easy true cases
        # case length compatible AND super- allows anything
        if is_sub_interval and \
            (is_dict_or_none(items2) or is_dict_or_true(addItems2)):
            return True
