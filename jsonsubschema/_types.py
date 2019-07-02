'''
Created on May 20, 2019
@author: Andrew Habib
'''

import sys
import math

import intervals as I

from abc import ABC

from _utils import(
    print_db,
    is_num,
    is_list,
    is_dict
)


class JsonType(ABC):

    def __init__(self):
        self.normalize()
        #
        self.isUninhabited = False
        self.check_uninhabited()
        if (self.isUninhabited):
            self.unInhabited_exit()

    def check_uninhabited(self):
        pass

    def unInhabited_exit(self):
        sys.exit("Found an uninhabited schema. Terminating ...")

    def normalize(self):
        pass


class JsonString(JsonType):

    def __init__(self, s):
        self.min = s.get("minLength")
        self.max = s.get("maxLength")
        self.pattern = s.get("pattern")
        #
        super().__init__()

    def check_uninhabited(self):
        if self.min > self.max:
            self.isInhibited = True
        # TODO
        # missing cases where min/max length might be
        # not compatible with pattern?


class JsonNumeric(JsonType):

    def __init__(self, s):
        self.type = s.get("type")
        self.min = s.get("minimum")
        self.xmin = s.get("exclusiveMinimum")
        self.max = s.get("maximum")
        self.xmax = s.get("exclusiveMaximum")
        self.mulOf = s.get("multipleOf")
        #
        self.interval = None
        self.build_interval_draft4()
        print_db(self.interval)
        #
        super().__init__()
        #

    def build_interval_draft4(self):
        pass

    def check_uninhabited(self):
        if self.interval:
            if self.interval.is_empty() or (self.mulOf != None and self.mulOf not in self.interval):
                self.isUninhabited = True

    @staticmethod
    def get_proper_JsonNumeric(s):
        if s.get("type") == "number":
            _s = JsonNumeric(s)
            if _s.mulOf and float(_s.mulOf).is_integer():
                s["type"] = "integer"
                if _s.min != -I.inf:
                    s["minimum"] = math.floor(
                        _s.min) if _s.xmin else math.ceil(_s.min)
                if _s.max != I.inf:
                    s["maximum"] = math.ceil(
                        _s.max) if _s.xmax else math.floor(_s.max)
                return JsonInteger(s)
            else:
                return JsonNumber(s)
        else:
            return JsonInteger(s)


class JsonNumber(JsonNumeric):

    def __init__(self, s):
        super().__init__(s)

    def build_interval_draft4(self):
        if self.xmin and self.xmax:
            self.interval = I.open(self.min, self.max)
        elif self.xmin:
            self.interval = I.openclosed(self.min, self.max)
        elif self.xmax:
            self.interval = I.closedopen(self.min, self.max)
        else:
            self.interval = I.closed(self.min, self.max)


class JsonInteger(JsonNumeric):

    def __init__(self, s):
        super().__init__(s)

    def build_interval_draft4(self):
        if self.xmin and self.xmax:
            self.interval = I.closed(self.min+1, self.max-1)
        elif self.xmin:
            self.interval = I.closed(self.min+1, self.max)
        elif self.xmax:
            self.interval = I.closed(self.min, self.max-1)
        else:
            self.interval = I.closed(self.min, self.max)


class JsonArray(JsonType):

    def __init__(self, s):
        self.items = s.get("items")
        self.min = s.get("minItems")
        self.max = s.get("maxItems")
        self.uniq = s.get("uniqueItems")
        self.addItems = s.get("additionalItems")
        #
        super().__init__()

    def normalize(self):
        self.compute_actual_max()

    def compute_actual_max(self):
        if is_list(self.items) and self.addItems == False:
            self.max = min(self.max, len(self.items))

    def check_uninhabited(self):
        if (is_list(self.items) and self.addItems == False
                and self.min > len(self.items)) \
           or (self.min > self.max):
            self.isUninhabited = True


class JsonObject(JsonType):

    def __init__(self, s):
        pass
