'''
Created on August 6, 2019
@author: Andrew Habib
'''

from setuptools import setup

setup(
    name='jsonsubschema',
    version='0.0.0',
    author='Andrew Habib, Avraham Shinnar, Martin Hirzel',
    author_email='andrew.a.habib@gmail.com',
    description="A tool to check whether a JSON schema is subschema of another JSON schema",
    long_description='For two JSON schemas s1 and s2, s1 <: s2 (read s1 is subtype or subschema of s2) \
                        if every instance that validates against s1 also validates against s2. \
                        This tool checks if one JSON schema is subtype of another.',
    url='https://github.com/IBM/json-subschema',
    packages=['jsonsubschema', ],
    license='Apache License 2.0',
    install_requires=['python-intervals', 'greenery', 'jsonschema'],
    entry_points={
        'console_scripts': 'jsonsubschema=jsonsubschema.cli:main'
    }
)
