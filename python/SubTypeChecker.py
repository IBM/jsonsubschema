'''
Created on May 20, 2019
@author: Andrew Habib
'''

import numbers
import greenery.lego as RegLib

from abc import ABC, abstractmethod

class SubTypeChecker(ABC):
    '''
    Goal: check if s1 <: s2
    for s1, s2 in json_types
    '''

    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
        super().__init__()

    @abstractmethod
    def is_subtype(self):
        pass

class Python_Types:
    @staticmethod
    def is_num(i):
        return isinstance(i, int) or isinstance(i, numbers.Number)

    @staticmethod
    def is_str(i):
        return isinstance(i. str)
