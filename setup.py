'''
Created on August 6, 2019
@author: Andrew Habib
'''

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(
    name='jsonsubschema',
    version='0.0.5',
    author='Andrew Habib, Avraham Shinnar, Martin Hirzel',
    author_email='andrew.a.habib@gmail.com',
    description="A tool to check whether a JSON schema is subset/subschema of another JSON schema",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/IBM/jsonsubschema',
    packages=['jsonsubschema', ],
    license='Apache License 2.0',
    install_requires=['portion', 'greenery', 'jsonschema', 'jsonref', 'numpy'],
    entry_points={
        'console_scripts': 'jsonsubschema=jsonsubschema.cli:main'
    }
)
