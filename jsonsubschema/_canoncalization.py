'''
Created on June 24, 2019
@author: Andrew Habib
'''
import copy
import numbers
import jsonschema

import _constants
from config import VALIDATOR
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
        return obj


def canoncalize_dict(d):
    if d == {}:
        return JSONEmptySchema()

    t = d.get("type")
    if isinstance(t, list):
        return canoncalize_list_of_types(d)
    elif isinstance(t, str):
        return canoncalize_single_type(d)
    elif "enum" in d.keys():
        return canoncalize_untyped_enum(d)
    elif set(d.keys()) & set(_constants.Jconnectors):
        return canoncalize_connectors(d)
    else:
        d["type"] = _constants.Jtypes
        return canoncalize_list_of_types(d)


def canoncalize_list_of_types(d):
    t = d.get("type")

    # if len(t) == 1:
    #     d["type"] = t[0]
    #     return canoncalize_single_type(d)

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


def canoncalize_single_type(d):
    t = d.get("type")
    if t in typeToConstructor.keys():
        # remove irrelevant keywords
        tmp = copy.deepcopy(d)
        for k, v in tmp.items():
            if k not in _constants.Jtypecommonkw and k not in _constants.JtypesToKeywords.get(t):
                d.pop(k)
            elif isinstance(v, dict):
                d[k] = canoncalize_dict(v)
            elif isinstance(v, list):
                # if entry in enum does not validate against outer schema,
                # remove it.
                if k == "enum":
                    for i in v:
                        try:
                            jsonschema.validate(instance=i, schema=tmp)
                        except:
                            d.get(k).remove(i)
                else:
                    d[k] = [canoncalize_dict(i) for i in v]
        return typeToConstructor[t](d)
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


def canoncalize_untyped_enum(d):
    t = set()
    for i in d.get("enum"):
        if isinstance(i, str):
            t.add("string")
        elif isinstance(i, int):
            t.add("integer")
        elif isinstance(i, float):
            t.add("number")
        elif isinstance(i, bool):
            t.add("boolean")
        elif isinstance(i, type(None)):
            t.add("null")
        elif isinstance(i, list):
            t.add("array")
        elif isinstance(i, dict):
            t.add("object")

    d["type"] = list(t)
    return canoncalize_list_of_types(d)
