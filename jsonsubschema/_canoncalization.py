'''
Created on June 24, 2019
@author: Andrew Habib
'''

import copy
import jsonschema
import numbers
import sys

import jsonsubschema._constants as definitions
import jsonsubschema._utils as utils
from jsonsubschema.config import VALIDATOR
from jsonsubschema._checkers import (
    typeToConstructor,
    boolToConstructor,
    negTypeToConstructor,
    JSONtop,
    JSONbot,
    JSONschema
)


def canonicalize_json(obj):
    if utils.is_dict(obj):
        return canonicalize_dict(obj)
    else:
        return obj


def canonicalize_dict(d, outer_key=None):

    # skip normal dict canonicalization
    # for object.properties/patternProperties
    # because these should be usual dict containers.
    if outer_key in ["properties", "patternProperties"]:
        for k, v in d.items():
            d[k] = canonicalize_dict(v)
        return d

    # here, start dict canonicalization
    if d == {} or not definitions.Jkeywords.intersection(d.keys()):
        return JSONtop()
    elif d.get("not") == {}:
        return JSONbot()

    t = d.get("type")
    has_connectors = definitions.Jconnectors.intersection(d.keys())

    # Start canoncalization.
    # Don't modify original dict.
    d = copy.deepcopy(d)

    if has_connectors:
        return canoncalize_connectors(d)
    elif utils.is_str(t):
        return canoncalize_single_type(d)
    elif utils.is_list(t):
        return canoncalize_list_of_types(d)
    elif "enum" in d.keys():
        return canoncalize_untyped_enum(d)
    else:
        d["type"] = definitions.Jtypes
        return canoncalize_list_of_types(d)


def canoncalize_single_type(d):
    t = d.get("type")
    if t in typeToConstructor.keys():
        # remove irrelevant keywords
        for k, v in list(d.items()):
            if k not in definitions.Jcommonkw and k not in definitions.JtypesToKeywords.get(t):
                d.pop(k)
            elif utils.is_dict(v):
                d[k] = canonicalize_dict(v, k)
            elif utils.is_list(v):
                if k == "enum":
                    v = utils.get_valid_enum_vals(v, d)
                    # if we have a schema with enum key and the
                    # enum does not have any valid value against the schema,
                    # then this entire schema with the enum is uninhabited
                    if v:
                        d[k] = v
                    else:
                        return JSONbot()
                elif k == "required":
                    # to order the list; for proper dict equality
                    d[k] = list(set(v))
                else:
                    d[k] = [canonicalize_dict(i) for i in v]
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
        if utils.is_str(i):
            t.add("string")
        elif utils.is_bool(i):
            t.add("boolean")
        elif utils.is_int(i):
            t.add("integer")
        elif utils.is_float(i):
            t.add("number")
        elif utils.is_null(i):
            t.add("null")
        elif utils.is_list(i):
            t.add("array")
        elif utils.is_dict(i):
            t.add("object")

    d["type"] = list(t)
    return canoncalize_list_of_types(d)


def canoncalize_connectors(d):
    connectors = definitions.Jconnectors.intersection(d.keys())
    lhs_kw = definitions.Jkeywords.intersection(d.keys())
    lhs_kw_without_connectors = lhs_kw.difference(connectors)

    # Single connector.
    if len(connectors) == 1 and not lhs_kw_without_connectors:
        c = connectors.pop()

        if c == "not":
            return canoncalize_not(d)

        else:
            d[c] = [canonicalize_dict(i) for i in d[c]]
            # Flatten nested connectors of the same type
            # This is not necessary currently.
            # TODO remove?
            for d_i in d[c]:
                if d_i.get(c):
                    d[c].extend(d_i.get(c))
                    d[c].remove(d_i)
            return boolToConstructor.get(c)(d)

    # Connector + other keywords. Combine them first.
    else:
        allofs = []
        for c in connectors:
            if c == "allOf":
                allofs.extend([canonicalize_dict(i) for i in d[c]])
            else:
                allofs.append(canonicalize_dict({c: d[c]}))
            del d[c]

        if lhs_kw_without_connectors:
            allofs.append(canonicalize_dict(d))
        return boolToConstructor.get("allOf")({"allOf": allofs})


def canoncalize_not(d):
    # d: {} has a not schema
    to_be_negated_schema = d["not"]
    if not isinstance(to_be_negated_schema, JSONschema):
        to_be_negated_schema = canonicalize_dict(to_be_negated_schema)

    # not schema is now in canonical form
    t = to_be_negated_schema.type
    if t in definitions.Jtypes:
        anyofs = []
        for t_i in definitions.Jtypes.difference([t]):
            anyofs.append(typeToConstructor.get(t_i)({"type": t_i}))
        anyofs.append(negTypeToConstructor.get(t)(to_be_negated_schema))
        anyofs = list(filter(None, anyofs))
        return boolToConstructor.get("anyOf")({"anyOf": anyofs})

    elif t in definitions.Jconnectors:

        if t == "not":
            return to_be_negated_schema

        if t == "anyOf":
            allofs = []
            for i in to_be_negated_schema["anyOf"]:
                allofs.append(canoncalize_not({"not": i}))
            return boolToConstructor.get("allOf")({"allOf": allofs})

        elif t == "allOf":
            anyofs = []
            for i in to_be_negated_schema["allOf"]:
                anyofs.append(canoncalize_not({"not": i}))
            return boolToConstructor.get("anyOf")({"anyOf": anyofs})

        elif t == "oneOf":
            sys.exit(">>>>>> oneOf is not supported yet. <<<<<<")
