'''
Created on May 20, 2019
@author: Andrew Habib
'''

import intervals as I
from SubTypeChecker import SubTypeChecker, Python_Types
from Utils import get_interval_from_json_number_draf4

is_num = Python_Types.is_num


class NumberSubTypeChecker(SubTypeChecker):

    def is_subtype(self):
        s1 = self.s1
        s2 = self.s2
        #
        i1 = get_interval_from_json_number_draf4(s1)
        i2 = get_interval_from_json_number_draf4(s2)
        is_sub_interval = i1 in i2
        #
        s1_mulOf = s1.get("multipleOf")
        s2_mulOf = s2.get("multipleOf")
        #
        if is_sub_interval and \
                (
                    (not is_num(s1_mulOf) and not is_num(s2_mulOf))
                    or (is_num(s1_mulOf) and not is_num(s2_mulOf))
                    or (is_num(s1_mulOf) and is_num(s2_mulOf) and s1_mulOf % s2_mulOf == 0)
                ):
            return True
        return False
