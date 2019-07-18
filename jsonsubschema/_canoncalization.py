'''
Created on June 24, 2019
@author: Andrew Habib
'''

import copy
import jsonschema
import numbers

import _constants
from config import VALIDATOR
from _checkers import (
    typeToConstructor,
    boolToConstructor,
    JSONtop,
    JSONbot
)


def canoncalize_json(obj):
    if isinstance(obj, dict):
        return canoncalize_dict(obj)
    else:
        # This can never happen as the schema validator, run prior to here,
        # does not accept anything but dictionaries.
        return obj


def canoncalize_dict(d):
    if d == {}:
        return JSONtop()

    t = d.get("type")
    has_connectors = set(d.keys()) & _constants.Jconnectors

    if has_connectors:
        return canoncalize_connectors(d)
    elif isinstance(t, str):
        return canoncalize_single_type(d)
    elif isinstance(t, list):
        return canoncalize_list_of_types(d)
    elif "enum" in d.keys():
        return canoncalize_untyped_enum(d)
    else:
        d["type"] = _constants.Jtypes
        return canoncalize_list_of_types(d)


def canoncalize_single_type(d):
    t = d.get("type")
    if t in typeToConstructor.keys():
        # remove irrelevant keywords
        for k, v in list(d.items()):
            if k not in _constants.Jtypecommonkw and k not in _constants.JtypesToKeywords.get(t):
                d.pop(k)
            elif isinstance(v, dict):
                d[k] = canoncalize_dict(v)
            elif isinstance(v, list):
                # if entry in enum does not validate against outer schema,
                # remove it.
                if k == "enum":
                    # continue
                    for i in v:
                        try:
                            jsonschema.validate(instance=i, schema=d)
                        except jsonschema.ValidationError:                            
                            d.get(k).remove(i)
                    else:
                        # if we have an outer schema and
                        # and enum without any valid value against the schema
                        # then this entire outer schema with the enum is uninhabited
                        if d.get(k) == []:
                            return JSONbot()
                else:
                    d[k] = [canoncalize_dict(i) for i in v]
        # if d.get("enum", None) == []:
        #     return
        return typeToConstructor[t](d)
    else:
        # TODO: or just return?
        print("Unknown schema type {} at:".format(t))
        print(d)
        print("Exiting...")
        sys.exit(1)


def canoncalize_list_of_types(d):
    t = d.get("type")

    # to save an unnecessary anyOf with one option only.
    if len(t) == 1:
        d["type"] = t.pop()
        return canoncalize_single_type(d)

    choices = []
    for t_i in t:
        if t_i in typeToConstructor.keys():
            s_i = copy.deepcopy(d)
            s_i["type"] = t_i
            s_i = canoncalize_single_type(s_i)
            choices.append(s_i)
        else:
            # TODO: or just return?
            print("Unknown schema type {} at: {}".format(t_i, t))
            print(d)
            print("Exiting...")
            sys.exit(1)
    d = {"anyOf": choices}
    # TODO do we need to return JSONanyOf ?
    return boolToConstructor.get("anyOf")(d)


def canoncalize_untyped_enum(d):
    t = set()
    for i in d.get("enum"):
        if isinstance(i, str):
            t.add("string")
        elif isinstance(i, bool):  # bool is subtype of int, so this check has to preceed int check
            t.add("boolean")
        elif isinstance(i, int):
            t.add("integer")
        elif isinstance(i, float):
            t.add("number")
        elif isinstance(i, type(None)):
            t.add("null")
        elif isinstance(i, list):
            t.add("array")
        elif isinstance(i, dict):
            t.add("object")

    d["type"] = list(t)
    return canoncalize_list_of_types(d)


def canoncalize_connectors(d):
    connectors = set(d.keys()) & _constants.Jconnectors
    lhs_kw = set(d.keys()) & _constants.Jkeywords_lhs
    lhs_kw_without_connectors = lhs_kw - connectors

    if len(connectors) == 1 and not lhs_kw_without_connectors:
        c = connectors.pop()
        d[c] = [canoncalize_dict(i) for i in d[c]]
        return boolToConstructor.get(c)(d)
    else:
        ret = {"allOf": []}

        for c in connectors:
            if c == "allOf":
                ret["allOf"].extend([canoncalize_dict(i) for i in d[c]])
            else:
                ret["allOf"].append(canoncalize_dict({c: d[c]}))
            del d[c]

        if lhs_kw_without_connectors:
            ret["allOf"].append(canoncalize_dict(d))

        return boolToConstructor.get("allOf")(ret)
