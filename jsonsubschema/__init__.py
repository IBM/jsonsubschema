"""
Created on August 6, 2019
@author: Andrew Habib
"""

from jsonsubschema import api
from jsonsubschema import config
from jsonsubschema import exceptions
from jsonsubschema import _canonicalization
from jsonsubschema import _explain

isSubschema = api.isSubschema
meetSchemas = api.meet
joinSchemas = api.join
isEquivalent = api.isEquivalent
schemaDiff = api.schemaDiff

canonicalizeSchema = _canonicalization.canonicalize_schema

set_debug = config.set_debug
set_warn_uninhabited = config.set_warn_uninhabited

is_subschema = api.isSubschema
is_subschema_with_reason = api.is_subschema_with_reason
SubschemaResult = _explain.SubschemaResult
