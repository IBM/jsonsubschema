'''
Created on May 20, 2019
@author: Andrew Habib
'''

import sys

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


class JsonNumeric(JsonType):

    key_words = ["minimum", "exclusiveMinimum",
                 "maximum", "exclusiveMaximum", "multipleOf"]

    def __init__(self, s):
        self.num_or_int = s.get("type") # what default to use?
        self.min = s.get("minimum", -I.inf)
        self.xmin = s.get("exclusiveMinimum", False)
        self.max = s.get("maximum", I.inf)
        self.xmax = s.get("exclusiveMaximum", False)
        self.mulOf = s.get("multipleOf")
        #
        super().__init__()
        #
        print_db(self.interval)

    def normalize(self):
        self.build_interval_draf4()
        #
        # if multipleOf is integer value, the schema can't accept numbers.
        # can't use isinstance(i, integer) because 5.0 is indeed integer!
        if self.mulOf != None and float.is_integer(float(self.mulOf)):
            self.num_or_int = "integer"

    def build_interval_draf4(self):
        _min = self.min
        _xmin = self.xmin
        _max = self.max
        _xmax = self.xmax
        #
        if _xmin and _xmax:
            i = I.open(_min, _max)
        elif _xmin:
            i = I.openclosed(_min, _max)
        elif _xmax:
            i = I.closedopen(_min, _max)
        else:
            i = I.closed(_min, _max)
        self.interval = i
        #
        # if is_num(_min) and is_num(_max):
        #     if _xmin and _xmax:
        #         i = I.open(_min, _max)
        #     elif _xmin and not _xmax:
        #         i = I.openclosed(_min, _max)
        #     elif not _xmin and _xmax:
        #         i = I.closedopen(_min, _max)
        #     else:
        #         i = I.closed(_min, _max)
        # elif is_num(_min) and not is_num(_max):
        #     if _xmin:
        #         i = I.open(_min, I.inf)
        #     else:
        #         i = I.closed(_min, I.inf)
        # elif not is_num(_min) and is_num(_max):
        #     if _xmax:
        #         i = I.open(-I.inf, _max)
        #     else:
        #         i = I.closed(-I.inf, _max)
        # elif not is_num(_min) and not is_num(_max):
        #     i = I.closed(-I.inf, I.inf)
        #
        # return i

    def check_uninhabited(self):
        if self.interval.is_empty() or \
                (self.mulOf != None and self.mulOf not in self.interval):
            self.isUninhabited = True


class JsonString(JsonType):

    key_words = ["minLength", "maxLength", "pattern"]

    def __init__(self, s):
        self.min = s.get("minLength", 0)
        self.max = s.get("maxLength", I.inf)
        self.pattern = s.get("pattern")
        #
        super().__init__()

    def check_uninhabited(self):
        if self.min > self.max:
            self.isInhibited = True
        # TODO
        # missing cases where min/max length might be
        # not compatible with pattern?


class JsonArray(JsonType):

    key_words = ["items", "minItems", "maxItems",
                 "uniqueItems", "additionalItems"]

    def __init__(self, s):
        # using default values eliminates extra checks for None!
        self.items = s.get("items", {})
        self.min = s.get("minItems", 0)
        self.max = s.get("maxItems", I.inf)
        self.uniq = s.get("uniqueItems", False)
        self.addItems = s.get("additionalItems", True)
        #
        super().__init__()

    def normalize(self):
        self.compute_actual_max()
        self.normalize_additionalItems()

    def normalize_additionalItems(self):
        if is_dict(self.items) or self.addItems == {}:
            self.addItems = True

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
