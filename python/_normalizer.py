'''
Created on June 7, 2019
@author: Andrew Habib
'''

import copy
import json
import jsonschema
import sys

from constants import(
    Jtypes,
    JtypesToKeywords,
    JkeywordsToDefaults,
    Jconnectors,
    Jcommonkw
)


def lazy_normalize(s):
    '''
    For now, I will apply the normalization as lazy as possible.
    I.e, this function should be explicitly called on each schema.
    The first two levels of a JSON schema is normalized. 
    Deeper levels, are normalized on demand!
    '''

    # Boolean connectors
    has_bool_connectors = set(s.keys()) & set(Jconnectors)
    if has_bool_connectors and len(has_bool_connectors) < len(s.keys()):
        s = rw_bool_connector(s)

    # Missing type
    t = s.get("type")
    if t is None and not has_bool_connectors:
        s["type"] = Jtypes

    # Singleton type
    t = s.get("type")
    if isinstance(t, list):
        s = rw_singleton_type(s)

    t = s.get("type")
    if isinstance(t, str):
        # Irrelevant keywords
        tmp_s = copy.deepcopy(s)
        for k, v in s.items():
            if k not in Jcommonkw and k not in JtypesToKeywords.get(t):
                tmp_s.pop(k)
                s = tmp_s

        # Default keywords
        for kw in JtypesToKeywords.get(t):
            if kw not in s.keys():
                s[kw] = JkeywordsToDefaults.get(kw)

    return s


def rw_bool_connector(s):
    _s = {}
    _s["allOf"] = []
    sub_no_connectors = {}
    for k, v in s.items():
        if k in Jconnectors:
            _v = []
            for v_i in v:
                _v.append(lazy_normalize(v_i))
            _s["allOf"].append({k: _v})
        else:
            sub_no_connectors[k] = v

    sub_no_connectors = lazy_normalize(sub_no_connectors)
    _s["allOf"].append(sub_no_connectors)
    return _s


def rw_singleton_type(s):
    choices = []
    for t_i in s.get("type"):
        s_i = copy.deepcopy(s)
        s_i["type"] = t_i
        s_i = lazy_normalize(s_i)
        choices.append(s_i)

    s = {"anyOf": choices}
    return s


if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        s = json.load(f)

    jsonschema.Draft4Validator.check_schema(s)
    print(s)

    s = lazy_normalize(s)
    print(s)
