'''
Created on May 24, 2019
@author: Andrew Habib
'''

import intervals as I
from greenery.lego import parse
from SubTypeChecker import SubTypeChecker, Python_Types
from Utils import is_sub_interval_from_optional_ranges

is_num = Python_Types.is_num


class StringSubTypeChecker(SubTypeChecker):

    def is_subtype(self):
        s1 = self.s1
        s2 = self.s2
        #
        min1 = s1.get("minLength")
        max1 = s1.get("maxLength")
        pattern1 = s1.get("pattern")
        #
        min2 = s2.get("minLength")
        max2 = s2.get("maxLength")
        pattern2 = s2.get("pattern")
        #
        is_sub_interval = is_sub_interval_from_optional_ranges(
            min1, max1, min2, max2)
        if not is_sub_interval:
            return False
        # at this point, length is compatible, so we should now worry about pattern only.
        if pattern2 == None or pattern2 == "":
            return True
        elif pattern1 == None or pattern1 == "":
            return False
        else:
            regex1 = parse(pattern1)
            regex2 = parse(pattern2)
            result = regex1 & regex2.everythingbut()
            if result.empty():
                return True
            else:
                return False
