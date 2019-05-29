'''
Created on May 20, 2019
@author: Andrew Habib
'''

import sys
from abc import ABC, abstractmethod


class JsonType(ABC):

    def __init__(self):
        self.isUninhabited = False
        if (self.check_uninhabited()):
            self.unInhabited_exit()

    @abstractmethod
    def check_uninhabited(self):
        pass

    unInhabited_exit = sys.exit("Found an inhibited type. Terminating ...")
