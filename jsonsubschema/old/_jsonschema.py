'''
Created on June 24, 2019
@author: Andrew Habib
'''

import copy
import json
import sys
import math
import numbers
import intervals as I
from abc import ABC, abstractmethod
from greenery.lego import parse
from intervals import inf as infinity


import config
import _constants
from canoncalization import canoncalize_object
from _normalizer import lazy_normalize

from _utils import (
    validate_schema,
    print_db,
    is_sub_interval_from_optional_ranges,
    is_num,
    is_list,
    is_dict,
    is_empty_dict_or_none,
    is_dict_or_true,
    one
)


class JSONschema(dict):

    kw_defaults = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.validate()
        self.updateKeys()
        # self.canoncalize()
        if self.isUninhabited():
            sys.exit("Found an uninhabited type at: " + str(self))

    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            raise AttributeError("No such attribute: ", name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            del self[name]
        else:
            raise AttributeError("No such attribute: ", name)

    def validate(self):
        validate_schema(self)

    def updateKeys(self):
        for k, v in self.kw_defaults.items():
            if k == "items":
                k = "items_"
            if k not in self.keys():
                self[k] = v

    def isBoolean(self):
        return self.keys() & _constants.Jconnectors

    def isUninhabited(self):
        return self._isUninhabited()

    def _isUninhabited(self):
        pass

    def meet(self, s2):
        pass

    def join(self, s2):
        pass

    def isSubtype(self, s2):
        if s2 == {} or s2 == True or self == s2:
            return True

        return self._isSubtype(s2)

    def isSubtype_handle_rhs(self, s2, isSubtype_cb):
        if s2.isBoolean():
            # TODO revisit all of this. They are wrong.
            if "anyOf" in s2:
                return any(self.isSubtype(s) for s in s2["anyOf"])
            elif "allOf" in s2:
                return all(self.isSubtype(s) for s in s2["allOf"])
            elif "oneOf" in s2:
                return one(self.isSubtype(s) for s in s2["oneOf"])
            elif "not" in s2:
                # TODO
                print("No handling of not yet.")
                return None
        else:
            print_db("cb on rhs")
            return isSubtype_cb(self, s2)


class JSONTypeString(JSONschema):

    kw_defaults = {"minLength": 0, "maxLength": infinity, "pattern": ".*"}

    def __init__(self, s):
        super().__init__(s)

    def _isUninhabited(self):
        return self.minLength > self.maxLength

    def meet(self, s):
        pass

    def _isSubtype(self, s2):

        def _isStringSubtype(self, s2):
            if s2.type != "string":
                return False

            is_sub_interval = is_sub_interval_from_optional_ranges(
                self.minLength, self.maxLength, s2.minLength, s2.maxLength)
            if not is_sub_interval:
                return False
            #
            # at this point, length is compatible,
            # so we should now worry about pattern only.
            if s2.pattern == None or s2.pattern == "":
                return True
            elif self.pattern == None or self.pattern == "":
                return False
            elif self.pattern == s2.pattern:
                return True
            else:
                regex = parse(self.pattern)
                regex2 = parse(s2.pattern)
                result = regex & regex2.everythingbut()
                if result.empty():
                    return True
                else:
                    return False

        return super().isSubtype_handle_rhs(s2, _isStringSubtype)


def JSONNumericFactory(s):
    if s.get("type") == "number":
        if s.get("multipleOf") and float(s.get("multipleOf")).is_integer():
            s["type"] = "integer"
            if s.get("minimum") != None:  # -I.inf:
                s["minimum"] = math.floor(s.get("minimum")) if s.get(
                    "exclusiveMinimum") else math.ceil(s.get("minimum"))
            if s.get("maximum") != None:  # I.inf:
                s["maximum"] = math.ceil(s.get("maximum")) if s.get(
                    "exclusiveMaximum") else math.floor(s.get("maximum"))
            return JSONTypeInteger(s)
        else:
            return JSONTypeNumber(s)
    else:
        return JSONTypeInteger(s)


class JSONTypeInteger(JSONschema):

    kw_defaults = {"minimum": -infinity, "maximum": infinity,
                   "exclusiveMinimum": False, "exclusiveMaximum": False, "multipleOf": None}

    def __init__(self, s):
        super().__init__(s)

    def build_interval_draft4(self):
        if self.exclusiveMinimum and self.exclusiveMaximum:
            self.interval = I.closed(self.minimum+1, self.maximum-1)
        elif self.exclusiveMinimum:
            self.interval = I.closed(self.minimum+1, self.maximum)
        elif self.exclusiveMaximum:
            self.interval = I.closed(self.minimum, self.maximum-1)
        else:
            self.interval = I.closed(self.minimum, self.maximum)

    def _isUninhabited(self):
        self.build_interval_draft4()
        return self.interval.is_empty() or \
            (self.multipleOf != None and self.multipleOf not in self.interval)

    def meet(self, s):
        pass

    def _isSubtype(self, s2):

        def _isIntegerSubtype(self, s2):
            if s2.type not in ["integer", "number"]:
                return False
            #
            is_sub_interval = self.interval in s2.interval
            if not is_sub_interval:
                print_db("num__00")
                return False
            #
            if (self.multipleOf == s2.multipleOf) \
                    or (self.multipleOf != None and s2.multipleOf == None) \
                    or (self.multipleOf != None and s2.multipleOf != None and self.multipleOf % s2.multipleOf == 0) \
                    or (self.multipleOf == None and s2.multipleOf == 1):
                print_db("num__02")
                return True

            if self.multipleOf == None and s2.multipleOf != None:
                return False

        return super().isSubtype_handle_rhs(s2, _isIntegerSubtype)


class JSONTypeNumber(JSONschema):
    kw_defaults = {"minimum": -infinity, "maximum": infinity,
                   "exclusiveMinimum": False, "exclusiveMaximum": False, "multipleOf": None}

    def __init__(self, s):
        super().__init__(s)

    def build_interval_draft4(self):
        if self.exclusiveMinimum and self.exclusiveMaximum:
            self.interval = I.open(self.minimum, self.maximum)
        elif self.exclusiveMinimum:
            self.interval = I.openclosed(self.minimum, self.maximum)
        elif self.exclusiveMaximum:
            self.interval = I.closedopen(self.minimum, self.maximum)
        else:
            self.interval = I.closed(self.minimum, self.maximum)

    def _isUninhabited(self):
        self.build_interval_draft4()
        return self.interval.is_empty() or \
            (self.multipleOf != None and self.multipleOf not in self.interval)

    def meet(self, s):
        pass

    def _isSubtype(self, s2):

        def _isNumberSubtype(self, s2):
            if s2.type != "number":
                return False
            #
            is_sub_interval = self.interval in s2.interval
            if not is_sub_interval:
                print_db("num__00")
                return False
            #
            if self.type == "number" and s2.type == "integer":
                print_db("num__01")
                return False
            #
            if (self.multipleOf == s2.multipleOf) \
                    or (self.multipleOf != None and s2.multipleOf == None) \
                    or (self.multipleOf != None and s2.multipleOf != None and self.multipleOf % s2.multipleOf == 0) \
                    or (self.multipleOf == None and s2.multipleOf == 1):
                print_db("num__02")
                return True

        return super().isSubtype_handle_rhs(s2, _isNumberSubtype)


class JSONTypeBoolean(JSONschema):
    kw_defaults = {}

    def __init__(self, s):
        super().__init__(s)

    def _isSubtype(self, s2):

        def _isBooleanSubtype(self, s2):
            if s2.type == "boolean":
                return True
            else:
                return False

        return super().isSubtype_handle_rhs(s2, _isBooleanSubtype)


class JSONTypeNull(JSONschema):
    kw_defaults = {}

    def __init__(self, s):
        super().__init__(s)

    def _isSubtype(self, s2):

        def _isNullSubtype(self, s2):
            if s2.type == "null":
                return True
            else:
                return False

        return super().isSubtype_handle_rhs(s2, _isNullSubtype)


class JSONTypeObject(JSONschema):

    kw_defaults = {"properties": {}, "additionalProperties": {}, "required": [
    ], "minProperties": 0, "maxProperties": infinity, "dependencies": {}, "patternProperties": {}}

    def __init__(self, s):
        super().__init__(s)

    def meet(self, s2):
        pass

    def _isSubtype(self, s2):

        def _isObjectSubtype(self, s2):
            pass

        return super().isSubtype_handle_rhs(s2, _isObjectSubtype)


class JSONTypeArray(JSONschema):

    kw_defaults = {"minItems": 0, "maxItems": infinity,
                   "items": JSONTypeObject({}), "additionalItems": JSONTypeObject({}), "uniqueItems": False}

    def __init__(self, s):
        super().__init__(s)

    def _isUninhabited(self):
        return (self.minItems > self.maxItems) or \
            (is_list(self.items) and self.additionalItems ==
             False and self.minItems > len(self.items))

    def meet(self, s2):
        pass

    def _isSubtype(self, s2):

        def _isArraySubtype(self, s2):
            print_db("in array subtype")
            if s2.type != "array":
                return False
            #
            #
            # self = JsonArray(self)
            # s2 = JsonArray(s2)
            #
            # uninhabited = handle_uninhabited_types(self, s2)
            # if uninhabited != None:
            #     return uninhabited
            #
            # -- minItems and maxItems
            is_sub_interval = is_sub_interval_from_optional_ranges(
                self.minItems, self.maxItems, s2.minItems, s2.maxItems)
            # also takes care of {'items' = [..], 'additionalItems' = False}
            if not is_sub_interval:
                print_db("__01__")
                return False
            #
            # -- uniqueItemsue
            # TODO Double-check. Could be more subtle?
            if not self.uniqueItems and s2.uniqueItems:
                print_db("__02__")
                return False
            #
            # -- items = {not empty}
            # no need to check additionalItems
            if is_dict(self.items_):
                if is_dict(s2.items_):
                    print_db(self.items_)
                    print_db(s2.items_)
                    # if subschemachecker.Checker.is_subtype(self.items_, s2.items_):
                    if self.items_.isSubtype(s2.items_):
                        print_db("__05__")
                        return True
                    else:
                        print_db("__06__")
                        return False
                elif is_list(s2.items_):
                    if s2.additionalItems == False:
                        print_db("__07__")
                        return False
                    elif s2.additionalItems == True:
                        for i in s2.items_:
                            # if not subschemachecker.Checker.is_subtype(self.items_, i):
                            if not self.items_.isSubtype(i):
                                print_db("__08__")
                                return False
                        print_db("__09__")
                        return True
                    elif is_dict(s2.additionalItems):
                        for i in s2.items_:
                            # if not subschemachecker.Checker.is_subtype(self.items_, i):
                            if not self.items_.isSubtype(i):
                                print_db("__10__")
                                return False
                        # if subschemachecker.Checker.is_subtype(self.items_, s2.additionalItems):
                        if self.items_.isSubtype(s2.additionalItems):
                            print_db("__11__")
                            return True
                        else:
                            print_db("__12__")
                            return False
            #
            elif is_list(self.items_):
                print_db("lhs is list")
                if is_dict(s2.items_):
                    if self.additionalItems == False:
                        for i in self.items_:
                            # if not subschemachecker.Checker.is_subtype(i, s2.items_):
                            if not i.isSubtype(s2.items_):
                                print_db("__13__")
                                return False
                        print_db("__14__")
                        return True
                    elif self.additionalItems == True:
                        for i in self.items_:
                            # if not subschemachecker.Checker.is_subtype(i, s2.items_):
                            if not i.isSubtype(s2.items_):
                                return False
                        return True
                    elif is_dict(self.additionalItems):
                        for i in self.items_:
                            # if not subschemachecker.Checker.is_subtype(i, s2.items_):
                            if not i.isSubtype(s2.items_):
                                return False
                        # if subschemachecker.Checker.is_subtype(self.additionalItems, s2.items_):
                        if self.additionalItems.isSubtype(s2.items_):
                            return True
                        else:
                            return False
                # now lhs and rhs are lists
                elif is_list(s2.items_):
                    print_db("lhs & rhs are lists")
                    len1 = len(self.items_)
                    len2 = len(s2.items_)
                    for i, j in zip(self.items_, s2.items_):
                        # if not subschemachecker.Checker.is_subtype(i, j):
                        if not i.isSubtype(j):
                            return False
                    if len1 == len2:
                        print_db("len1 == len2")
                        if self.additionalItems == s2.additionalItems:
                            return True
                        elif self.additionalItems == True and s2.additionalItems == False:
                            return False
                        elif self.additionalItems == False and s2.additionalItems == True:
                            return True
                        else:
                            # return subschemachecker.Checker.is_subtype(self.additionalItems, s2.additionalItems)
                            return self.additionalItems.isSubtype(s2.additionalItems)
                    elif len1 > len2:
                        diff = len1 - len2
                        for i in range(len1-diff, len1):
                            # if not subschemachecker.Checker.is_subtype(self.items_[i], s2.additionalItems):
                            if not self.items_[i].isSubtype(s2.additionalItems):
                                print_db("9999")
                                return False
                        print_db("8888")
                        return True
                    else:  # len2 > len 1
                        # if self.additionalItems:
                        diff = len2 - len1
                        for i in range(len2 - diff, len2):
                            print_db("self.additionalItems",
                                     self.additionalItems)
                            print_db(i, s2.items_[i])
                            # if not subschemachecker.Checker.is_subtype(self.additionalItems, s2.items_[i]):
                            if not self.additionalItems.isSubtype(s2.items_[i]):
                                print_db("!!!")
                                return False
                        # return subschemachecker.Checker.is_subtype(self.additionalItems, s2.additionalItems)
                        return self.additionalItems.isSubtype(s2.additionalItems)

        return super().isSubtype_handle_rhs(s2, _isArraySubtype)


class JSONanyOf(JSONschema):

    def meet(self, s):
        pass

    def _isSubtype(self, s2):

        def _isAnyofSubtype(self, s2):
            for s in self.anyOf:
                if not s.isSubtype(s2):
                    return False
            return True

        return super().isSubtype_handle_rhs(s2, _isAnyofSubtype)


class JSONallOf(JSONschema):

    def meet(self, s):
        pass

    def _isSubtype(Self, s2):

        def _isAllOfSubtype(self, s2):
            for s in self.allOf:
                if not s.isSubtype(s2):
                    return False
            return True

        return super().isSubtype_handle_rhs(s2, _isAllOfSubtype)


class JSONoneOf(JSONschema):

    def meet(self, s):
        pass

    def _isSubtype(self, s2):
        sys.exit("onOf on the lhs is not supported yet.")

class JSONnot(JSONschema):
    
    def meet(self, s):
        pass

    def _isSubtype(self, s):
        pass
typeToConstructor = {
    "string": JSONTypeString,
    "integer": JSONNumericFactory,
    "number": JSONNumericFactory,
    "boolean": JSONTypeBoolean,
    "null": JSONTypeNull,
    "array": JSONTypeArray,
    "object": JSONTypeObject
}

boolToConstructor = {
    "anyOf": JSONanyOf,
    "allOf": JSONallOf,
    "oneOf": JSONoneOf,
    "not": JSONnot
}


class JSONSchemaSubtypeFactory(json.JSONDecoder):

    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(
            self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, d):
        print_db("object before canon.", d)
        # return JSONSchemaSubtypeFactory.canoncalize_object(d)
        return canoncalize_object(d)
    
    # @staticmethod
    # def canoncalize_object(d):
    #     validate_schema(d)
    #     if d == {}:
    #         return d
    #     t = d.get("type")
    #     if isinstance(t, list):
    #         return JSONSchemaSubtypeFactory.canoncalize_list_of_types(d)
    #     elif isinstance(t, str):
    #         return JSONSchemaSubtypeFactory.canoncalize_single_type(d)
    #     else:
    #         connectors = set(d.keys()) & set(_constants.Jconnectors)
    #         if connectors:
    #             return JSONSchemaSubtypeFactory.canoncalize_connectors(d)
    #         else:
    #             d["type"] = _constants.Jtypes
    #             return JSONSchemaSubtypeFactory.canoncalize_list_of_types(d)
    
    # @staticmethod
    # def canoncalize_list_of_types(d):
    #     t = d.get("type")
    #     choices = []
    #     for t_i in t:
    #         if t_i in typeToConstructor.keys():
    #             s_i = copy.deepcopy(d)
    #             s_i["type"] = t_i
    #             s_i = JSONSchemaSubtypeFactory.canoncalize_single_type(s_i)
    #             choices.append(s_i)
    #         else:
    #             print("Unknown schema type {} at:".format(t))
    #             print(d)
    #             print("Exiting...")
    #             sys.exit(1)
    #     d = {"anyOf": choices}
    #     # TODO do we need to return JSONanyOf ?
    #     return boolToConstructor.get("anyOf")(d)

    # @staticmethod
    # def canoncalize_single_type(d):
    #     t = d.get("type")
    #     # check type is known
    #     if t in typeToConstructor.keys():
    #         # remove irrelevant keywords
    #         tmp = copy.deepcopy(d)
    #         for k in tmp.keys():
    #             if k not in _constants.Jcommonkw and k not in _constants.JtypesToKeywords.get(t):
    #                 d.pop(k)
    #         return typeToConstructor[t](d)
    #     else:
    #         print("Unknown schema type {} at:".format(t))
    #         print(d)
    #         print("Exiting...")
    #         sys.exit(1)

    # @staticmethod
    # def canoncalize_connectors(d):
    #     # TODO
    #     connectors = set(d.keys()) & set(_constants.Jconnectors)
    #     if len(connectors) == 1:
    #         return boolToConstructor[connectors.pop()](d)
    #     elif len(connectors) > 1:
    #         return boolToConstructor["allOf"]({"allOf": list({k: v} for k, v in d.items())})
    #     else:
    #         print("Something went wrong")


class JSONSubtypeChecker:
    
    def __init__(self, s1, s2):
        # validate_schema(s1)
        # validate_schema(s2)
        self.s1 = self.canoncalize_json(s1)
        self.s2 = self.canoncalize_json(s2)

    def canoncalize_json(self, obj):
        if isinstance(obj, str) or isinstance(obj, numbers.Number) or isinstance(obj, bool) or isinstance(obj, type(None)) or isinstance(obj, list):
            return obj
        elif isinstance(obj, dict):
            # return JSONSchemaSubtypeFactory.canoncalize_object(obj)
            return canoncalize_object(obj)

    def isSubtype(self):
        return self.s1.isSubtype(self.s2)


if __name__ == "__main__":

    s1_file = sys.argv[1]
    s2_file = sys.argv[2]
    print("Loading json schemas from:\n{}\n{}\n".format(s1_file, s2_file))

    #######################################
    
    with open(s1_file, 'r') as f1:
        s1 = json.load(f1, cls=JSONSchemaSubtypeFactory)
    with open(s2_file, 'r') as f2:
        s2 = json.load(f2, cls=JSONSchemaSubtypeFactory)
    print(s1)
    print(s2)
    print("Usage scenario 1:", s1.isSubtype(s2))

    #######################################

    with open(s1_file, 'r') as f1:
        s1 = json.load(f1)
    with open(s2_file, 'r') as f2:
        s2 = json.load(f2)
    print(s1)
    print(s2)
    print("Usage scenario 2:", JSONSubtypeChecker(s1, s2).isSubtype())