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
from jsonsubschema._checkers import (
    typeToConstructor,
    boolToConstructor,
    JSONtop,
    JSONbot
)

TOP = {}
BOT = {"not": {}}


def canonicalize_schema(obj):
    # First, make sure the given json is a valid json schema.
    utils.validate_schema(obj)

    # Second, canonicalize the schema.
    if utils.is_dict(obj):
        canonical_schema = canonicalize_dict(obj)

    # Finally, ensure that canonicalized schema is till a valid json schema.
    utils.validate_schema(canonical_schema)

    return canonical_schema


def canonicalize_dict(d, outer_key=None):
    # Skip normal dict canonicalization
    # for object.properties/patternProperties
    # because these should be usual dict containers.
    if outer_key in ["properties", "patternProperties"]:
        for k, v in d.items():
            d[k] = canonicalize_dict(v)
        return d

    # here, start dict canonicalization
    if not definitions.Jkeywords.intersection(d.keys()):
        return TOP

    t = d.get("type")
    has_connectors = definitions.Jconnectors.intersection(d.keys())

    # Start canonicalization. Don't modify original dict.
    d = copy.deepcopy(d)

    if "enum" in d.keys():
        return canonicalize_enum(d)
    elif has_connectors:
        return canonicalize_connectors(d)
    elif utils.is_str(t):
        return canonicalize_single_type(d)
    elif utils.is_list(t):
        return canonicalize_list_of_types(d)
    else:
        d["type"] = definitions.Jtypes
        return canonicalize_list_of_types(d)


def canonicalize_single_type(d):
    t = d.get("type")
    if t in definitions.Jtypes:
        # Remove irrelevant keywords
        for k, v in list(d.items()):
            if k not in definitions.Jcommonkw and k not in definitions.JtypesToKeywords.get(t):
                d.pop(k)
            elif utils.is_dict(v):
                d[k] = canonicalize_dict(v, k)
            elif utils.is_list(v):
                if k == "enum":
                    v = utils.get_typed_enum_vals(v, t)
                    if not v:
                        return BOT
                    else:
                        d[k] = v
                elif k == "required":
                    d[k] = sorted(set(v))
                else:
                    # "list" must be operand of boolean connectors
                    d[k] = [canonicalize_dict(i) for i in v]
        if "enum" in d:
            return rewrite_enum(d)
        else:
            return d

    else:
        # TODO: or just return?
        print("Unknown schema type {} at:".format(t))
        print(d)
        print("Exiting...")
        sys.exit(1)


def canonicalize_list_of_types(d):
    t = sorted(d.get("type"))
    anyofs = []
    for t_i in t:
        if t_i in definitions.Jtypes:
            s_i = copy.deepcopy(d)
            s_i["type"] = t_i
            s_i = canonicalize_single_type(s_i)
            anyofs.append(s_i)
        else:
            # TODO: or just return?
            print("Unknown schema type {} at: {}".format(t_i, t))
            print(d)
            print("Exiting...")
            sys.exit(1)

    return flatten_boolean_schema_with_one_operand({"anyOf": anyofs})


def canonicalize_enum(d):
    valid_vals = utils.get_valid_enum_vals(d["enum"], d)
    if not valid_vals:
        return BOT

    d["enum"] = valid_vals
    actual_t = sorted(
        set(map(lambda i: definitions.PyTypesToJtypes.get(type(i)), d.get("enum"))))
    if "type" in d:
        orig_t = d["type"]
        orig_t = set([orig_t]) if utils.is_str(orig_t) else set(orig_t)
        d["type"] = orig_t.intersection(actual_t)
    else:
        d["type"] = actual_t
    return canonicalize_list_of_types(d)


def canonicalize_connectors(d):
    connectors = definitions.Jconnectors.intersection(d.keys())
    lhs_kw = definitions.Jkeywords.intersection(d.keys())
    lhs_kw_without_connectors = lhs_kw.difference(connectors)

    # Single connector.
    if len(connectors) == 1 and not lhs_kw_without_connectors:
        c = connectors.pop()

        if c == "not":
            d["not"] = canonicalize_dict(d["not"])
            return canonicalize_not(d)

        elif c == "oneOf":
            if len(d[c]) == 1:
                return canonicalize_dict(d[c].pop())
            anyofs = []
            for i in range(len(d[c])):
                one = [d[c][i]]
                nots = [{"not": j} for j in d[c][:i]] + [{"not": j}
                                                         for j in d[c][i+1:]]
                allofs = one + nots
                anyofs.append({"allOf": allofs})
            return canonicalize_connectors({"anyOf": anyofs})
        else:
            d[c] = [canonicalize_dict(i) for i in d[c]]
            return flatten_boolean_schema_with_one_operand(d)

    # Connector + other keywords. Combine them first.
    else:
        allofs = []
        for c in connectors:
            allofs.append(canonicalize_dict({c: d[c]}))
            del d[c]
        if lhs_kw_without_connectors:
            allofs.append(canonicalize_dict(d))
        return flatten_boolean_schema_with_one_operand({"allOf": allofs})


def canonicalize_not(d):
    # d: {} has a 'not' schema
    negated_schema = d["not"]

    t = negated_schema.get("type")

    # if "enum" in negated_schema:
    #     return canonicalize_negated_enum(negated_schema)

    if negated_schema == {} or t in definitions.Jtypes:
        return d

    connectors = definitions.Jconnectors.intersection(negated_schema.keys())
    if connectors and len(connectors) == 1:
        c = connectors.pop()
        # Case "not: {"not": {...}}
        # Return positive schema (2 nots cancel each other)
        if c == "not":
            return negated_schema["not"]

        if c == "anyOf":
            allofs = []
            for i in negated_schema["anyOf"]:
                allofs.append(canonicalize_not({"not": i}))
            return flatten_boolean_schema_with_one_operand({"allOf": allofs})

        elif c == "allOf":
            anyofs = []
            for i in negated_schema["allOf"]:
                anyofs.append(canonicalize_not({"not": i}))
            return flatten_boolean_schema_with_one_operand({"anyOf": anyofs})

        elif c == "oneOf":
            return canonicalize_not({"not": canonicalize_connectors(negated_schema)})
    else:
        sys.exit(">>>>>> Ewwwww! Shouldn't be here during canonicalization. <<<<<<")


def canonicalize_negated_enum(d):
    t = d.get("type")
    enum = d.get("enum")
    assert t in definitions.Jtypes and enum != None, "Ewwwwwwwww canonicalize_negated_enum"

    if t == "string":
        pattern = "|".join(map(lambda x: "^"+str(x)+"$", enum))
        ret = {"not": {"type": "string", "pattern": pattern}}

    return canonicalize_dict(ret)


def rewrite_enum(d):
    t = d.get("type")
    enum = d.get("enum")
    ret = None

    if t == "string":
        pattern = "|".join(map(lambda x: "^"+str(x)+"$", enum))
        ret = {"type": "string", "pattern": pattern}

    if t == "integer":
        ret = {"anyOf": []}
        for i in enum:
            ret["anyOf"].append(
                {"type": "integer", "minimum": i, "maximum": i})

    if t == "number":
        ret = {"anyOf": []}
        for i in enum:
            if utils.is_int_equiv(i):
                ret["anyOf"].append(
                    {"type": "integer", "minimum": i, "maximum": i})
            else:
                ret["anyOf"].append(
                    {"type": "number", "minimum": i, "maximum": i})

    if t == "boolean":
        return d

    if t == "null":
        return {"type": "null"}

    if ret:
        return canonicalize_dict(ret)
    else:
        return d


def flatten_boolean_schema_with_one_operand(s):
    c = definitions.Jconnectors.difference(["not"]).intersection(s.keys())
    assert len(
        c) == 1, "Ewwwww. This should be called only if schema has one and only once connector that is not 'not'"
    c = c.pop()
    flat = []
    for i in s[c]:
        if c in i:
            flat.extend(i[c])
        else:
            flat.append(i)

    if len(flat) == 0:
        return BOT
    elif len(flat) == 1:
        return flat.pop()
    else:
        return {c: flat}


def simplify_schema_and_embed_checkers(s):
    ''' This function assumes the schema s is already canonicalized. 
        So it must be a dict '''
    #
    if s == {}:
        return JSONtop()
    if s == {"not": {}}:
        return JSONbot()

    # json.array specific
    if "items" in s:
        if utils.is_dict(s["items"]):
            s["items"] = simplify_schema_and_embed_checkers(s["items"])
        elif utils.is_list(s["items"]):
            s["items"] = [simplify_schema_and_embed_checkers(
                i) for i in s["items"]]

    if "additionalItems" in s and utils.is_dict(s["additionalItems"]):
        s["additionalItems"] = simplify_schema_and_embed_checkers(
            s["additionalItems"])

    # json.object specific
    if "properties" in s:
        s["properties"] = dict([(k, simplify_schema_and_embed_checkers(v))
                                for k, v in s["properties"].items()])

    if "patternProperties" in s:
        s["patternProperties"] = dict([(k, simplify_schema_and_embed_checkers(
            v)) for k, v in s["patternProperties"].items()])

    if "additionalProperties" in s and utils.is_dict(s["additionalProperties"]):
        s["additionalProperties"] = simplify_schema_and_embed_checkers(
            s["additionalProperties"])

    #
    if "type" in s:
        return typeToConstructor.get(s["type"])(s)

    if "not" in s:
        return typeToConstructor.get(s["not"]["type"]).neg(s["not"])

    if "anyOf" in s:
        anyofs = [simplify_schema_and_embed_checkers(i) for i in s["anyOf"]]
        return boolToConstructor.get("anyOf")({"anyOf": anyofs})

    if "allOf" in s:
        allofs = [simplify_schema_and_embed_checkers(i) for i in s["allOf"]]
        return boolToConstructor.get("allOf")({"allOf": allofs})
