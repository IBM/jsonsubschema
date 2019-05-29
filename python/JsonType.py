'''
Created on May 20, 2019
@author: Andrew Habib
'''

from abc import ABC, abstractmethod


class JsonType(ABC):

    def __init__(self):
        self.isInhibited = False
        self.check_inhibited()

    @abstractmethod
    def check_inhibited(self):
        pass
