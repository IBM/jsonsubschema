'''
Created on May 11, 2020
@author: Andrew Habib
'''


class _Error(Exception):
    pass


class UnexpectedCanonicalization(_Error):

    def __init__(self, msg, tau, schema):
        self.msg = msg
        self.tau = tau
        self.schema = schema

    def __str__(self):
        return '{}\n"type": {} \n"schema": {}'.format(self.msg, self.tau, self.schema)


# class UnsupportedSchemaType(_Error):
#     '''
#     Probably this is not required since custom types are not
#     supported by jsonschema validation anyways; so we will not reat
#     a case that uses this exception.'''

#     def __init__(self, schema, tau):
#         self.schema = schema
#         self.tau = tau

#     def __str__(self):
#         return '{} is unsupported jsonschema type in schema: {}'.format(self.tau, self.schema)


# class UnsupportedSubtypeChecker(_Error):

#     def __init__(self, schema, desc):
#         self.schema = schema
#         self.desc = desc

#     def __str__(self):
#         return '{} is unsupported. Schema: {}'.format(self.desc, self.schema)
