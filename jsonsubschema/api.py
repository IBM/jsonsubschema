"""
Created on June 24, 2019
@author: Andrew Habib
"""

import sys
import jsonref

from jsonsubschema._canonicalization import (
    canonicalize_schema,
    simplify_schema_and_embed_checkers,
)
from jsonsubschema._utils import validate_schema, print_db

from jsonsubschema.exceptions import UnsupportedRecursiveRef


def prepare_operands(s1, s2):
    # First, we load schemas using jsonref to resolve $ref
    # before starting canonicalization.

    # s1 = jsonref.loads(json.dumps(s1))
    # s2 = jsonref.loads(json.dumps(s2))
    # This is not very efficient, should be done lazily maybe?
    s1 = jsonref.JsonRef.replace_refs(s1)
    s2 = jsonref.JsonRef.replace_refs(s2)

    # Canonicalize and embed checkers for both lhs
    # and rhs schemas  before starting the subtype checking.
    # This also validates input schemas and canonicalized schemas.

    # At the moment, recursive/circual refs are not supported and hence, canonicalization
    # throws a RecursionError.
    try:
        _s1 = simplify_schema_and_embed_checkers(canonicalize_schema(s1))
    except RecursionError:
        # avoid cluttering output by unchaining the recursion error
        raise UnsupportedRecursiveRef(s1, "LHS") from None

    try:
        _s2 = simplify_schema_and_embed_checkers(canonicalize_schema(s2))
    except RecursionError:
        # avoid cluttering output by unchaining the recursion error
        raise UnsupportedRecursiveRef(s2, "RHS") from None

    return _s1, _s2


def isSubschema(s1, s2):
    """Entry point for schema subtype checking."""
    s1, s2 = prepare_operands(s1, s2)
    return s1.isSubtype(s2)


def meet(s1, s2):
    """Entry point for schema meet operation."""
    s1, s2 = prepare_operands(s1, s2)
    return s1.meet(s2)


def join(s1, s2):
    """Entry point for schema meet operation."""
    s1, s2 = prepare_operands(s1, s2)
    return s1.join(s2)


def isEquivalent(s1, s2):
    """Entry point for schema equivalence check operation."""
    return isSubschema(s1, s2) and isSubschema(s2, s1)


def schemaDiff(s1, s2):
    """Analyze the compatibility relationship between two schemas.

    Returns one of:
    - 'equivalent': s1 <: s2 and s2 <: s1
    - 'backward_compatible': s1 <: s2 (s1 is more restrictive)
    - 'forward_compatible': s2 <: s1 (s2 is more restrictive)
    - 'breaking': neither direction holds
    - 'unknown': an unsupported feature prevented the check
    """
    from jsonsubschema.exceptions import _UnsupportedCase

    try:
        fwd = isSubschema(s1, s2)
    except _UnsupportedCase:
        fwd = None

    try:
        bwd = isSubschema(s2, s1)
    except _UnsupportedCase:
        bwd = None

    if fwd is None or bwd is None:
        if fwd is True and bwd is True:
            return "equivalent"
        elif fwd is True:
            return "backward_compatible"
        elif bwd is True:
            return "forward_compatible"
        return "unknown"

    if fwd and bwd:
        return "equivalent"
    elif fwd:
        return "backward_compatible"
    elif bwd:
        return "forward_compatible"
    else:
        return "breaking"


def is_subschema_with_reason(s1, s2):
    """
    Check if s1 is a subschema of s2, with detailed failure reasons.

    Returns a SubschemaResult containing:
    - is_subtype: bool indicating if s1 <: s2
    - reasons: list of failure reasons if is_subtype is False
    """
    from jsonsubschema._explain import ExplainContext, SubschemaResult

    ctx = ExplainContext()
    ExplainContext.set_current(ctx)
    try:
        _s1, _s2 = prepare_operands(s1, s2)
        result = _s1.isSubtype(_s2)
        return SubschemaResult(
            is_subtype=result, reasons=ctx.reasons if not result else []
        )
    finally:
        ExplainContext.set_current(None)
