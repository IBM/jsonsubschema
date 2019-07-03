'''
Created on June 24, 2019
@author: Andrew Habib
'''
import copy
import numbers

import _constants
from _checkers import (
    typeToConstructor,
    boolToConstructor,
    JSONEmptySchema
)


def canoncalize_json(obj):
    if isinstance(obj, dict):
        return canoncalize_dict(obj)
    else:
        # This can never happen as the schema validator, run prior to here,
        # does not accept anything but dictionaries.
        return


def canoncalize_dict(d):
    if d == {}:
        return JSONEmptySchema()

    t = d.get("type")
    if isinstance(t, list):
        return canoncalize_list_of_types(d)
    elif isinstance(t, str):
        return canoncalize_single_type(d)
    else:
        connectors = set(d.keys()) & set(_constants.Jconnectors)
        if connectors:
            return canoncalize_connectors(d)
        else:
            d["type"] = _constants.Jtypes
            return canoncalize_list_of_types(d)


def canoncalize_list_of_types(d):
    t = d.get("type")
    choices = []
    for t_i in t:
        if t_i in typeToConstructor.keys():
            s_i = copy.deepcopy(d)
            s_i["type"] = t_i
            s_i = canoncalize_single_type(s_i)
            choices.append(s_i)
        else:
            # TODO: or just return?
            print("Unknown schema type {} at:".format(t))
            print(d)
            print("Exiting...")
            sys.exit(1)
    d = {"anyOf": choices}
    # TODO do we need to return JSONanyOf ?
    return boolToConstructor.get("anyOf")(d)


def canoncalize_single_type(d):
    t = d.get("type")
    if t in typeToConstructor.keys():
        # remove irrelevant keywords
        tmp = copy.deepcopy(d)
        for k, v in d.items():
            if k not in _constants.Jcommonkw and k not in _constants.JtypesToKeywords.get(t):
                tmp.pop(k)
            if isinstance(v, dict):
                tmp[k] = canoncalize_dict(v)
            if isinstance(v, list):
                tmp[k] = [canoncalize_dict(i) for i in v]
        return typeToConstructor[t](tmp)
    else:
        # TODO: or just return?
        print("Unknown schema type {} at:".format(t))
        print(d)
        print("Exiting...")
        sys.exit(1)


def canoncalize_connectors(d):
    # TODO
    connectors = set(d.keys()) & set(_constants.Jconnectors)
    if len(connectors) == 1:
        return boolToConstructor[connectors.pop()](d)
    elif len(connectors) > 1:
        return boolToConstructor["allOf"]({"allOf": list({k: v} for k, v in d.items())})
    else:
        print("Something went wrong")
