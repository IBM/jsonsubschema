'''
Created on June 24, 2019
@author: Andrew Habib
'''

import copy
import itertools
import json
import math
import numbers
import sys

import intervals as I

import config
import _constants

from _utils import (
    print_db,
    regex_meet,
    regex_isSubset,
    lcm,
    is_num,
    is_bool,
    is_list,
    is_dict,
    one
)


class UninhabitedMeta(type):

    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.checkUninhabited()
        return obj


class JSONschema(dict, metaclass=UninhabitedMeta):

    kw_defaults = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Since some of the default values for JSON types
        # are not compatible with the jsonschema validator, 
        # we don't explicitly add the keys with default values
        # to the underlying dict.
        # self.updateKeys()


    def __getattr__(self, name):

        if name in self:
            return self[name]
        # hack for JSONarray items because the inherit from dict
        # which also has a method named dict.items()
        elif name == "items_":
            if "items" in self.keys():
                return self["items"]
            elif "items" in self.kw_defaults:
                return self.kw_defaults["items"]
            else:
                raise AttributeError("Couldn't find items_: ", name)
                
        elif name in self.kw_defaults:
            return self.kw_defaults[name]    
        else:
            raise AttributeError("No such attribute: ", name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        if name in self:
            if name == "items_":
                del self["items"]
            else:
                del self[name]
        else:
            raise AttributeError("No such attribute: ", name)

    def updateKeys(self):
        for k, v in self.kw_defaults.items():
            if k not in self.keys():
                self[k] = v
        # dirty hack becuase self.items() is already an attribute of dict
        if "items" in self.keys():
            self["items_"] = self["items"]
            del self["items"]

    def isBoolean(self):
        return self.keys() & _constants.Jconnectors

    def checkUninhabited(self):
        self.uninhabited = self._isUninhabited()
        if config.WARN_UNINHABITED and self.uninhabited and not is_bot(self):
            print("Found an uninhabited type at: ", type(self), str(self))

    def meet(self, s):
        #
        if self == s or is_top(s):
            return self
        #
        if is_top(self):
            return s
        #
        if is_bot(self) or is_bot(s):
            return JSONbot()
        #
        ret = self._meet(s)
        # instead of returning uninhabited types, return bot
        if is_bot(ret):
            return JSONbot()
        else:
            return ret

    def meet_handle_rhs(self, s, meet_cb):
        #
        if s.type == "anyOf":
            return JSONanyOf._meetAnyOf(s, self)
        #
        else:
            return meet_cb(self, s)
        
    def join(self, s):
        #
        if self == s or is_bot(s): 
            return self
        #
        if is_bot(self):
            return s
        #
        if is_top(self) or is_top(s):
            return JSONtop()
        #
        ret = self._join(s)
        # instead of returning uninhabited types, return bot
        if is_bot(ret):
            return JSONbot()
        else:
            return ret
        

    def isSubtype(self, s):
        #
        if self == s or is_bot(self) or is_top(s):
            return True
        #
        if not is_bot(self) and is_bot(s):
            return False
        #
        return self._isSubtype(s)

    def isSubtype_handle_rhs(self, s, isSubtype_cb):
        if s.isBoolean():
            # TODO revisit all of this. They are wrong.
            if s.type == "anyOf":
                return any(isSubtype_cb(self, i) for i in s.anyOf)
            elif s.type == "allOf":
                return all(isSubtype_cb(self, i) for i in s.allOf)
            elif s.type == "oneOf":
                return one(isSubtype_cb(self, i) for i in s.oneOf)
            elif s.type  == "not":
                # TODO
                print("No handling of 'not' on rhs yet.")
                return None
        else:
            return isSubtype_cb(self, s)


class JSONtop(JSONschema):

    def _isUninhabited(self):
        return False

    def _meet(self, s):
        return s

    def _isSubtype(self, s):

        def _isTopSubtype(s1, s2):
            if is_top(s2):
                return True
            return False

        super().isSubtype_handle_rhs(s, _isTopSubtype)

    def __repr__(self):
        return "JSON_TOP"

def is_top(obj):
    return isinstance(obj, JSONtop) or obj == True


class JSONbot(JSONschema):

    def _isUninhabited(self):
        return True

    def _meet(self, s):
        return self

    def _isSubtype(self, s):

        def _isBotSubtype(s1, s2):
            if is_bot(s2):
                return True
            return False

        super().isSubtype_handle_rhs(s, _isBotSubtype)

    def __repr__(self):
        return "JSON_BOT"

def is_bot(obj):
    return isinstance(obj, JSONbot) or obj == False \
        or (isinstance(obj, JSONschema) and obj.uninhabited)


class JSONTypeString(JSONschema):

    kw_defaults = {"type": "string", "minLength": 0,
                   "maxLength": I.inf, "pattern": ".*"}

    def __init__(self, s):
        super().__init__(s)

    def _isUninhabited(self):
        self.interval = I.closed(self.minLength, self.maxLength)
        return (self.minLength > self.maxLength) or self.pattern == None

    def _meet(self, s):
        
        def _meetString(s1, s2):
            if s2.type == "string":
                ret = {}
                ret["minLength"] = max(s1.minLength, s2.minLength)
                ret["maxLength"] = min(s1.maxLength, s2.maxLength)
                ret["pattern"] = regex_meet(s1.pattern, s2.pattern)
                return JSONTypeString(ret)
            else:
                return JSONbot()

        return super().meet_handle_rhs(s, _meetString)

    def _isSubtype(self, s):

        def _isStringSubtype(s1, s2):
            if s2.type == "string":
                is_sub_interval = s1.interval in s2.interval
                if not is_sub_interval:
                    return False
                #
                # at this point, length is compatible,
                # so we should now worry about pattern only.
                if s2.pattern == None or s2.pattern == "":
                    return True
                elif s1.pattern == None or s1.pattern == "":
                    return False
                elif s1.pattern == s2.pattern:
                    return True
                else:
                    if regex_isSubset(s1.pattern, s2.pattern):
                        return True
                    else:
                        return False
            else:
                return False

        return super().isSubtype_handle_rhs(s, _isStringSubtype)


def JSONNumericFactory(s):
    '''Factory method handle the case of JSON number with multipleOf being integer.
        In this case, the JSON number becomes a JSON integer.'''

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

def isNumericUninhabited(s):
    return s.interval.is_empty()  \
    or (s.multipleOf != None and s.multipleOf not in s.interval
        and s.interval.lower != -I.inf and s.interval.upper != I.inf)

class JSONTypeInteger(JSONschema):

    kw_defaults = {"type": "integer", "minimum": -I.inf, "maximum": I.inf,
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
        return isNumericUninhabited(self)

    def _meet(self, s):

        def _meetInteger(s1, s2):
            if s2.type in _constants.Jnumeric:
                ret = {}
                ret["type"] = "integer"
                ret["minimum"] = max(s1.minimum, s2.minimum)
                ret["maximum"] = min(s1.maximum, s2.maximum)
                ret["multipleOf"] = lcm(s1.multipleOf, s2.multipleOf)
                return JSONTypeInteger(ret)
            else:
                return JSONbot()
        
        return super().meet_handle_rhs(s, _meetInteger)

    def _isSubtype(self, s):

        def _isIntegerSubtype(s1, s2):
            if s2.type in _constants.Jnumeric:
                #
                is_sub_interval = s1.interval in s2.interval
                if not is_sub_interval:
                    print_db("num__00")
                    return False
                #
                if (s1.multipleOf == s2.multipleOf) \
                        or (s1.multipleOf != None and s2.multipleOf == None) \
                        or (s1.multipleOf != None and s2.multipleOf != None and s1.multipleOf % s2.multipleOf == 0) \
                        or (s1.multipleOf == None and s2.multipleOf == 1):
                    print_db("num__02")
                    return True
                #
                if s1.multipleOf == None and s2.multipleOf != None:
                    return False
            else:
                return False

        return super().isSubtype_handle_rhs(s, _isIntegerSubtype)


class JSONTypeNumber(JSONschema):

    kw_defaults = {"type": "number", "minimum": -I.inf, "maximum": I.inf,
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
        return isNumericUninhabited(self)

    def _meet(self, s):
        
        def _meetNumber(s1, s2):
            if s2.type in _constants.Jnumeric:
                ret = {}
                ret["type"] = "integer" if s2.type == "integer" else "number"
                ret["minimum"] = max(s1.minimum, s2.minimum)
                ret["maximum"] = min(s1.maximum, s2.maximum)
                ret["multipleOf"] = lcm(s1.multipleOf, s2.multipleOf)
                return JSONNumericFactory(ret)
            else:
                return JSONbot()
        
        return super().meet_handle_rhs(s, _meetNumber)


    def _isSubtype(self, s):

        def _isNumberSubtype(s1, s2):
            if s2.type == "number":
                is_sub_interval = s1.interval in s2.interval
                if not is_sub_interval:
                    print_db("num__00")
                    return False
                #
                if (s1.multipleOf == s2.multipleOf) \
                        or (s1.multipleOf != None and s2.multipleOf == None) \
                        or (s1.multipleOf != None and s2.multipleOf != None and s1.multipleOf % s2.multipleOf == 0) \
                        or (s1.multipleOf == None and s2.multipleOf == 1):
                    print_db("num__02")
                    return True
            else:
                return False

        return super().isSubtype_handle_rhs(s, _isNumberSubtype)


class JSONTypeBoolean(JSONschema):

    kw_defaults = {"type": "boolean"}

    def __init__(self, s):
        super().__init__(s)

    def _isUninhabited(self):
        return False

    def _meet(self, s):

        def _meetBoolean(s1, s2):
            if s2.type == "boolean":
                return s1
            else:
                return JSONbot()

        return super().meet_handle_rhs(s, _meetBoolean)

    def _isSubtype(self, s):

        def _isBooleanSubtype(self, s2):
            if s2.type == "boolean":
                return True
            else:
                return False

        return super().isSubtype_handle_rhs(s, _isBooleanSubtype)


class JSONTypeNull(JSONschema):

    kw_defaults = {"type": "null"}

    def __init__(self, s):
        super().__init__(s)

    def _isUninhabited(self):
        return False

    def _meet(self, s):

        def _meetNull(s1, s2):
                
            if s2.type == "null":
                return s1
            else:
                return JSONbot()

        return super().meet_handle_rhs(s, _meetNull)

    def _isSubtype(self, s):

        def _isNullSubtype(self, s2):
            if s2.type == "null":
                return True
            else:
                return False

        return super().isSubtype_handle_rhs(s, _isNullSubtype)


class JSONTypeArray(JSONschema):

    kw_defaults = {"type": "array", "minItems": 0, "maxItems": I.inf,
                   "items": JSONtop(), "additionalItems": JSONtop(), "uniqueItems": False}

    def __init__(self, s):
        super().__init__(s)

    def compute_actual_maxItems(self):
        if is_list(self.items_) and \
                (self.additionalItems == False or (is_dict(self.additionalItems) and self.additionalItems.uninhabited)):
            self.maxItems = min(self.maxItems, len(self.items_))

    def _isUninhabited(self):
        self.compute_actual_maxItems()
        self.interval = I.closed(self.minItems, self.maxItems)
        return (self.minItems > self.maxItems) or \
            (is_list(self.items_) and self.additionalItems ==
             False and self.minItems > len(self.items_)) or \
            (is_list(self.items_) and len(self.items_) == 0)

    def _meet(self, s):

        def _meetArray(s1, s2):
            if s2.type == "array":
                ret = {}
                ret["type"] = "array"
                ret["minItems"] = max(s1.minItems, s2.minItems)
                ret["maxItems"] = min(s1.maxItems, s2.maxItems)
                ret["uniqueItems"] = s1.uniqueItems or s2.uniqueItems

                def meet_arrayItems_dict_list(s1, s2, ret):
                    assert is_dict(s1.items_) and is_list(
                        s2.items_), "Violating meet_arrayItems_dict_list condition: 's1.items is dict' and 's2.items is list'"
                    itms = []
                    for i in s2.items_:
                        r = i.meet(s1.items_)
                        if not (is_bot(r) or r.uninhabited):
                            itms.append(r)
                        else:
                            break

                    ret["items"] = itms

                    if s2.additionalItems == True:
                        ret["additionalItems"] = copy.deepcopy(s1.items_)
                    elif s2.additionalItems == False:
                        ret["additionalItems"] = False
                    elif is_dict(s2.additionalItems):
                        ad = copy.deepcopy(s2.additionalItems)
                        ad = ad.meet(s1.items_)
                        ret["additionalItems"] = False if is_bot(ad) else ad
                    return ret

                if is_dict(s1.items_):

                    if is_dict(s2.items_):
                        i = copy.deepcopy(s1.items_)
                        i = i.meet(s2.items_)
                        ret["items"] = i
                        ret["additionalItems"] = True

                    elif is_list(s2.items_):
                        ret = meet_arrayItems_dict_list(s1, s2, ret)

                elif is_list(s1.items_):

                    if is_dict(s2.items_):
                        ret = meet_arrayItems_dict_list(s2, s1, ret)

                    elif is_list(s2.items_):
                        self_len = len(s1.items_)
                        s_len = len(s2.items_)

                        def meet_arrayAdditionalItems_list_list(s1, s2):
                            if is_bool(s1.additionalItems) and is_bool(s2.additionalItems):
                                ad = s1.additionalItems and s2.additionalItems
                            elif is_dict(s1.additionalItems):
                                ad = s1.additionalItems.meet(s2.additionalItems)
                            elif is_dict(s2.additionalItems):
                                ad = s2.additionalItems.meet(s1.additionalItems)
                            return False if is_bot(ad) else ad

                        def meet_array_longlist_shorterlist(s1, s2, ret):
                            s1_len = len(s1.items_)
                            s2_len = len(s2.items_)
                            assert s1_len > s2_len, "Violating meet_array_longlist_shorterlist condition: 's1.len > s2.len'"
                            itms = []
                            for i, j in zip(s1.items_, s2.items_):
                                r = i.meet(j)
                                if not (is_bot(r) or r.uninhabited):
                                    itms.append(r)
                                else:
                                    ad = False
                                    break
                            else:
                                for i in range(s2_len, s1_len):
                                    r = s1.items_[i].meet(s2.additionalItems)
                                    if not (is_bot(r) or r.uninhabited):
                                        itms.append(r)
                                    else:
                                        ad = False
                                        break
                                else:
                                    ad = meet_arrayAdditionalItems_list_list(s1, s2)

                            ret["additionalItems"] = ad
                            ret["items"] = itms
                            return ret

                        if self_len == s_len:
                            itms = []
                            for i, j in zip(s1.items_, s2.items_):
                                r = i.meet(j)
                                if not (is_bot(r) or r.uninhabited):
                                    itms.append(r)
                                else:
                                    ad = False
                                    break
                            else:
                                ad = meet_arrayAdditionalItems_list_list(s1, s2)

                            ret["additionalItems"] = ad
                            ret["items"] = itms

                        elif self_len > s_len:
                            ret = meet_array_longlist_shorterlist(s1, s2, ret)

                        elif self_len < s_len:
                            ret = meet_array_longlist_shorterlist(s2, s1, ret)

                return JSONTypeArray(ret)
            
            else:
                return JSONbot()
            
        return super().meet_handle_rhs(s, _meetArray)

    def _isSubtype(self, s):

        def _isArraySubtype(s1, s2):
            if s2.type != "array":
                return False
            #
            # -- minItems and maxItems
            is_sub_interval = s1.interval in s2.interval
            if not is_sub_interval:
                print_db("__01__")
                return False
            #
            # -- uniqueItemsue
            # TODO Double-check. Could be more subtle?
            if not s1.uniqueItems and s2.uniqueItems:
                print_db("__02__")
                return False
            #
            # -- items = {not empty}
            # no need to check additionalItems
            if is_dict(s1.items_):
                if is_dict(s2.items_):
                    print_db(s1.items_)
                    print_db(s2.items_)
                    if s1.items_.isSubtype(s2.items_):
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
                            if not s1.items_.isSubtype(i):
                                print_db("__08__")
                                return False
                        print_db("__09__")
                        return True
                    elif is_dict(s2.additionalItems):
                        for i in s2.items_:
                            if not s1.items_.isSubtype(i):
                                print_db("__10__")
                                return False
                        print_db(type(s1.items_), s1.items_)
                        print_db(type(s2.additionalItems), s2.additionalItems)
                        if s1.items_.isSubtype(s2.additionalItems):
                            print_db("__11__")
                            return True
                        else:
                            print_db("__12__")
                            return False
            #
            elif is_list(s1.items_):
                print_db("lhs is list")
                if is_dict(s2.items_):
                    if s1.additionalItems == False:
                        for i in s1.items_:
                            if not i.isSubtype(s2.items_):
                                print_db("__13__")
                                return False
                        print_db("__14__")
                        return True
                    elif s1.additionalItems == True:
                        for i in s1.items_:
                            if not i.isSubtype(s2.items_):
                                return False
                        return True
                    elif is_dict(s1.additionalItems):
                        for i in s1.items_:
                            if not i.isSubtype(s2.items_):
                                return False
                        if s1.additionalItems.isSubtype(s2.items_):
                            return True
                        else:
                            return False
                # now lhs and rhs are lists
                elif is_list(s2.items_):
                    print_db("lhs & rhs are lists")
                    len1 = len(s1.items_)
                    len2 = len(s2.items_)
                    for i, j in zip(s1.items_, s2.items_):
                        if not i.isSubtype(j):
                            return False
                    if len1 == len2:
                        print_db("len1 == len2")
                        if s1.additionalItems == s2.additionalItems:
                            return True
                        elif s1.additionalItems == True and s2.additionalItems == False:
                            return False
                        elif s1.additionalItems == False and s2.additionalItems == True:
                            return True
                        else:
                            return s1.additionalItems.isSubtype(s2.additionalItems)
                    elif len1 > len2:
                        diff = len1 - len2
                        for i in range(len1-diff, len1):
                            if s2.additionalItems == False:
                                return False
                            elif s2.additionalItems == True:
                                return True
                            elif not s1.items_[i].isSubtype(s2.additionalItems):
                                print_db("9999")
                                return False
                        print_db("8888")
                        return True
                    else:  # len2 > len 1
                        diff = len2 - len1
                        for i in range(len2 - diff, len2):
                            if s1.additionalItems == False:
                                return True
                            elif s1.additionalItems == True:
                                return False
                            elif not s1.additionalItems.isSubtype(s2.items_[i]):
                                return False
                        return s1.additionalItems.isSubtype(s2.additionalItems)

        return super().isSubtype_handle_rhs(s, _isArraySubtype)


class JSONTypeObject(JSONschema):

    kw_defaults = {"properties": {}, "additionalProperties": {}, "required": [],
                   "minProperties": 0, "maxProperties": I.inf, "dependencies": {}, "patternProperties": {}}

    def __init__(self, s):
        super().__init__(s)

    def _isUninhabited(self):
        # TODO
        return False

    def _meet(self, s):

        def _meetObject(s1, s2):
            if s2.type == "object":
                # TODO
                # object meet
                pass
            else:
                return JSONbot()
            
        return super().meet_handle_rhs(s, _meetObject)

    def _isSubtype(self, s):

        def _isObjectSubtype(s1, s2):
            # TODO
            return

        return super().isSubtype_handle_rhs(s, _isObjectSubtype)


class JSONanyOf(JSONschema):

    kw_defaults = {"type": "anyOf"}

    def __init__(self, s):
        super().__init__(s)

    def _isUninhabited(self):
        return all(i.uninhabited for i in self.anyOf)

    def _meet(self, s):
        
        return super().meet_handle_rhs(s, JSONanyOf._meetAnyOf)
        

    @staticmethod
    def _meetAnyOf(s1, s2):        
        anyofs = []
        for i in s1.anyOf:
            tmp = i.meet(s2)
            if not is_bot(tmp):
                anyofs.append(tmp)

        if len(anyofs) > 1:
            return JSONanyOf({"anyOf": anyofs})
        elif len(anyofs) == 1:
            return anyofs.pop()
        else:
            return JSONbot()
    

    def _isSubtype(self, s):

        def _isAnyofSubtype(s1, s2):
            for s in s1.anyOf:
                if not s.isSubtype(s2):
                    return False
            return True

        return _isAnyofSubtype(self, s)


def JSONallOfFactory(s):
    ret = JSONtop()
    for i in s.get("allOf"):
        ret = ret.meet(i)
    return ret


class JSONallOf(JSONschema):

    kw_defaults = {"type": "allOf"}

    def __init__(self, s):
        super().__init__(s)

    def _isUninhabited(self):
        return any(i.uninhabited for i in self.allOf)

    def _meet(self, s):
        allofs = []
        for i in self.allOf:
            allofs.append(i.meet(s))

        return JSONallOfFactory({"allOf": allofs})

    def _isSubtype(Self, s):

        def _isAllOfSubtype(self, s2):
            for s in self.allOf:
                if not s.isSubtype(s2):
                    return False
            return True

        return _isAllOfSubtype(self, s)


class JSONoneOf(JSONschema):

    kw_defaults = {"type": "oneOf"}

    def __init__(self, s):
        super().__init__(s)

    def _isUninhabited(self):
        return False

    def _meet(self, s):
        pass

    def _isSubtype(self, s):
        sys.exit("oneOf on the lhs is not supported yet.")


class JSONnot(JSONschema):

    kw_defaults = {"type": "not"}
    
    def __init__(self, s):
        super().__init__(s)

    def _meet(self, s):
        pass

    def _isSubtype(self, s):
        sys.exit("not is not supported yet.")


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
    "allOf": JSONallOfFactory,
    # "oneOf": JSONoneOf,
    # "not": JSONnot
}
