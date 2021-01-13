
import numpy
import unittest
import json

import jsonsubschema
# from jsonsubschema.exp_dircmp import run_issubset

class TestAIExamples(unittest.TestCase):

    lrOld_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'description': 'Input data schema for training.',
        'type': 'object',
        'required': ['X', 'y'],
        'additionalProperties': False,
        'properties': {
            'X': {
                'description': 'Features; the outer array is over samples.',
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'number'}}},
            'y': {
                'description': 'Target class labels; the array is over samples.',
                'type': 'array',
                'items': {
                    'type': 'number'}}}
    }

    lrNew_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'description': 'Input data schema for training.',
        'type': 'object',
        'required': ['X', 'y'],
        'additionalProperties': False,
        'properties': {
            'X': {
                'description': 'Features; the outer array is over samples.',
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'number'}}},
            'y': {
                'description': 'Target class labels; the array is over samples.',
                "anyOf": [
                    {"type": "array", "items": {"type": "number"}},
                    {"type": "array", "items": {"type": "string"}},
                    {"type": "array", "items": {"type": "boolean"}}]}}
    }

    project_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'description': 'Input data schema for training Project.',
        'type': 'object',
        'required': ['X'],
        'additionalProperties': False,
        'properties': {
            'X': {
                'description': 'Features; the outer array is over samples.',
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': {
                        'anyOf': [{
                            'type': 'number'}, {
                            'type': 'string'}]}}},
            'y': {
                'description': 'Target class labels; the array is over samples.'}}
    }

    nmf_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'required': ['X'],
        'additionalProperties': False,
        'properties': {
            'X': {
                'type': 'array',
                'items': {
                    'type': 'array',
                    'items': {
                        'type': 'number',
                        'minimum': 0.0}}},
            'y': {}}
    }

    tfidf_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'description': 'Input data schema for training the TfidfVectorizer from scikit-learn.',
        'type': 'object',
        'required': ['X'],
        'additionalProperties': False,
        'properties': {
            'X': {
                'description': 'Features; the outer array is over samples.',
                'anyOf': [{
                    'type': 'array',
                    'items': {
                        'type': 'string'}}, {
                    'type': 'array',
                    'items': {
                        'type': 'array',
                        'minItems': 1,
                        'maxItems': 1,
                        'items': {
                            'type': 'string'}}}]},
            'y': {
                'description': 'Target class labels; the array is over samples.'}}
    }

    irisArr_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'additionalProperties': False,
        'required': ['X', 'y'],
        'properties': {
            'X': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'minItems': 150,
                'maxItems': 150,
                'items': {
                    'type': 'array',
                    'minItems': 4,
                    'maxItems': 4,
                    'items': {
                        'type': 'number'}}},
            'y': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'minItems': 150,
                'maxItems': 150,
                'items': {
                    'type': 'integer'}}}
    }

    irisDf_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'additionalProperties': False,
        'required': ['X', 'y'],
        'properties': {
            'X': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'minItems': 120,
                'maxItems': 120,
                'items': {
                    'type': 'array',
                    'minItems': 4,
                    'maxItems': 4,
                    'items': [
                        {'description': 'sepal length (cm)', 'type': 'number'},
                        {'description': 'sepal width (cm)', 'type': 'number'},
                        {'description': 'petal length (cm)', 'type': 'number'},
                        {'description': 'petal width (cm)', 'type': 'number'}]}},
            'y': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'minItems': 120,
                'maxItems': 120,
                'items': {
                    'description': 'target',
                    'type': 'integer'}}}
    }

    digits_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'additionalProperties': False,
        'required': ['X', 'y'],
        'properties': {
            'X': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'items': {
                    'type': 'array',
                    'minItems': 64,
                    'maxItems': 64,
                    'items': {
                        'type': 'number',
                        'minimum': 0,
                        'maximum': 16}},
                'minItems': 1437,
                'maxItems': 1437},
            'y': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'minItems': 1437,
                'maxItems': 1437,
                'items': {
                    'description': 'target',
                    'type': 'integer'}}}
    }

    housing_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'additionalProperties': False,
        'required': ['X', 'y'],
        'properties': {
            'X': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'items': {
                    'type': 'array',
                    'minItems': 8,
                    'maxItems': 8,
                    'items': [
                        {'description': 'MedInc', 'type': 'number', 'minimum': 0.0},
                        {'description': 'HouseAge', 'type': 'number', 'minimum': 0.0},
                        {'description': 'AveRooms', 'type': 'number', 'minimum': 0.0},
                        {'description': 'AveBedrms', 'type': 'number', 'minimum': 0.0},
                        {'description': 'Population', 'type': 'number', 'minimum': 0.0},
                        {'description': 'AveOccup', 'type': 'number', 'minimum': 0.0},
                        {'description': 'Latitude', 'type': 'number', 'minimum': 0.0},
                        {'description': 'Longitude', 'type': 'number'}]},
                'minItems': 16512,
                'maxItems': 16512},
            'y': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'minItems': 16512,
                'maxItems': 16512,
                'items': {
                    'description': 'target',
                    'type': 'number'}}}
    }

    creditG_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'additionalProperties': False,
        'required': ['X', 'y'],
        'properties': {
            'X': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'minItems': 670,
                'maxItems': 670,
                'items': {
                    'type': 'array',
                    'minItems': 20,
                    'maxItems': 20,
                    'items': [
                        {'description': 'checking_status', 'enum': ['<0', '0<=X<200', '>=200', 'no checking']},
                        {'description': 'duration', 'type': 'number'},
                        {'description': 'credit_history', 'enum': ['no credits/all paid', 'all paid', 'existing paid', 'delayed previously', 'critical/other existing credit']},
                        {'description': 'purpose', 'enum': ['new car', 'used car', 'furniture/equipment', 'radio/tv', 'domestic appliance', 'repairs', 'education', 'vacation', 'retraining', 'business', 'other']},
                        {'description': 'credit_amount', 'type': 'number'},
                        {'description': 'savings_status', 'enum': ['<100', '100<=X<500', '500<=X<1000', '>=1000', 'no known savings']},
                        {'description': 'employment', 'enum': ['unemployed', '<1', '1<=X<4', '4<=X<7', '>=7']},
                        {'description': 'installment_commitment', 'type': 'number'},
                        {'description': 'personal_status', 'enum': ['male div/sep', 'female div/dep/mar', 'male single', 'male mar/wid', 'female single']},
                        {'description': 'other_parties', 'enum': ['none', 'co applicant', 'guarantor']},
                        {'description': 'residence_since', 'type': 'number'},
                        {'description': 'property_magnitude', 'enum': ['real estate', 'life insurance', 'car', 'no known property']},
                        {'description': 'age', 'type': 'number'},
                        {'description': 'other_payment_plans', 'enum': ['bank', 'stores', 'none']},
                        {'description': 'housing', 'enum': ['rent', 'own', 'for free']},
                        {'description': 'existing_credits', 'type': 'number'},
                        {'description': 'job', 'enum': ['unemp/unskilled non res', 'unskilled resident', 'skilled', 'high qualif/self emp/mgmt']},
                        {'description': 'num_dependents', 'type': 'number'},
                        {'description': 'own_telephone', 'enum': ['none', 'yes']},
                        {'description': 'foreign_worker', 'enum': ['yes', 'no']}]}},
            'y': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'minItems': 670,
                'maxItems': 670,
                'items': {
                    'description': 'class',
                    'enum': [0, 1]}}}
    }

    movies_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'additionalProperties': False,
        'required': ['X', 'y'],
        'properties': {
            'X': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'minItems': 10662,
                'maxItems': 10662,
                'items': {
                    'type': 'string'}},
            'y': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'minItems': 10662,
                'maxItems': 10662,
                'items': {
                    'type': 'integer'}}}
    }

    drugRev_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'additionalProperties': False,
        'required': ['X', 'y'],
        'properties': {
            'X': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'items': {
                    'type': 'array',
                    'minItems': 5,
                    'maxItems': 5,
                    'items': [
                        {'description': 'drugName', 'type': 'string'},
                        {'description': 'condition', 'anyOf': [{'type': 'string'}, {'enum': [numpy.NaN]}]},
                        {'description': 'review', 'type': 'string'},
                        {'description': 'date', 'type': 'string'},
                        {'description': 'usefulCount', 'type': 'integer', 'minimum': 0}]},
                'minItems': 161297,
                'maxItems': 161297},
            'y': {
                '$schema': 'http://json-schema.org/draft-04/schema#',
                'type': 'array',
                'items': {
                    'description': 'rating',
                    'enum': [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]},
                'minItems': 161297,
                'maxItems': 161297}}
    }

    adultCat_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'additionalProperties': False,
        'required': ['X', 'y'],
        'properties': {
            'X': {
                'type': 'array',
                'minItems': 32724, 'maxItems': 32724,
                'items': {
                    'type': 'array',
                    'minItems': 14, 'maxItems': 14,
                    'items': [
                        {'description': 'age', 'type': 'number'},
                        {'description': 'workclass', 'type': 'string'},
                        {'description': 'fnlwgt', 'type': 'number'},
                        {'description': 'education', 'type': 'string'},
                        {'description': 'education-num', 'type': 'number'},
                        {'description': 'marital-status', 'type': 'string'},
                        {'description': 'occupation', 'type': 'string'},
                        {'description': 'relationship', 'type': 'string'},
                        {'description': 'race', 'type': 'string'},
                        {'description': 'sex', 'type': 'string'},
                        {'description': 'capital-gain', 'type': 'number'},
                        {'description': 'capital-loss', 'type': 'number'},
                        {'description': 'hours-per-week', 'type': 'number'},
                        {'description': 'native-country', 'type': 'string'}]}},
            'y': {
                'type': 'array',
                'minItems': 32724, 'maxItems': 32724,
                'items': {'description': 'class', 'enum': ['<=50K', '>50K']}}}}

    adultNum_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'type': 'object',
        'additionalProperties': False,
        'required': ['X', 'y'],
        'properties': {
            'X': {
                'type': 'array',
                'minItems': 32724, 'maxItems': 32724,
                'items': {
                    'type': 'array',
                    'minItems': 105, 'maxItems': 105,
                    'items': [
                        {'description': 'workclass_Federal-gov', 'enum': [0,1]},
                        {'description': 'workclass_Local-gov', 'enum': [0,1]},
                        {'description': 'workclass_Never-worked', 'enum': [0,1]},
                        {'description': 'workclass_Private', 'enum': [0,1]},
                        {'description': 'workclass_Self-emp-inc', 'enum': [0,1]},
                        {'description': 'workclass_Self-emp-not-inc', 'enum': [0,1]},
                        {'description': 'workclass_State-gov', 'enum': [0,1]},
                        {'description': 'workclass_Without-pay', 'enum': [0,1]},
                        {'description': 'education_10th', 'enum': [0,1]},
                        {'description': 'education_11th', 'enum': [0,1]},
                        {'description': 'education_12th', 'enum': [0,1]},
                        {'description': 'education_1st-4th', 'enum': [0,1]},
                        {'description': 'education_5th-6th', 'enum': [0,1]},
                        {'description': 'education_7th-8th', 'enum': [0,1]},
                        {'description': 'education_9th', 'enum': [0,1]},
                        {'description': 'education_Assoc-acdm', 'enum': [0,1]},
                        {'description': 'education_Assoc-voc', 'enum': [0,1]},
                        {'description': 'education_Bachelors', 'enum': [0,1]},
                        {'description': 'education_Doctorate', 'enum': [0,1]},
                        {'description': 'education_HS-grad', 'enum': [0,1]},
                        {'description': 'education_Masters', 'enum': [0,1]},
                        {'description': 'education_Preschool', 'enum': [0,1]},
                        {'description': 'education_Prof-school', 'enum': [0,1]},
                        {'description': 'education_Some-college', 'enum': [0,1]},
                        {'description': 'marital-status_Divorced', 'enum': [0,1]},
                        {'description': 'marital-status_Married-AF-spouse', 'enum': [0,1]},
                        {'description': 'marital-status_Married-civ-spouse', 'enum': [0,1]},
                        {'description': 'marital-status_Married-spouse-absent', 'enum': [0,1]},
                        {'description': 'marital-status_Never-married', 'enum': [0,1]},
                        {'description': 'marital-status_Separated', 'enum': [0,1]},
                        {'description': 'marital-status_Widowed', 'enum': [0,1]},
                        {'description': 'occupation_Adm-clerical', 'enum': [0,1]},
                        {'description': 'occupation_Armed-Forces', 'enum': [0,1]},
                        {'description': 'occupation_Craft-repair', 'enum': [0,1]},
                        {'description': 'occupation_Exec-managerial', 'enum': [0,1]},
                        {'description': 'occupation_Farming-fishing', 'enum': [0,1]},
                        {'description': 'occupation_Handlers-cleaners', 'enum': [0,1]},
                        {'description': 'occupation_Machine-op-inspct', 'enum': [0,1]},
                        {'description': 'occupation_Other-service', 'enum': [0,1]},
                        {'description': 'occupation_Priv-house-serv', 'enum': [0,1]},
                        {'description': 'occupation_Prof-specialty', 'enum': [0,1]},
                        {'description': 'occupation_Protective-serv', 'enum': [0,1]},
                        {'description': 'occupation_Sales', 'enum': [0,1]},
                        {'description': 'occupation_Tech-support', 'enum': [0,1]},
                        {'description': 'occupation_Transport-moving', 'enum': [0,1]},
                        {'description': 'relationship_Husband', 'enum': [0,1]},
                        {'description': 'relationship_Not-in-family', 'enum': [0,1]},
                        {'description': 'relationship_Other-relative', 'enum': [0,1]},
                        {'description': 'relationship_Own-child', 'enum': [0,1]},
                        {'description': 'relationship_Unmarried', 'enum': [0,1]},
                        {'description': 'relationship_Wife', 'enum': [0,1]},
                        {'description': 'race_Amer-Indian-Eskimo', 'enum': [0,1]},
                        {'description': 'race_Asian-Pac-Islander', 'enum': [0,1]},
                        {'description': 'race_Black', 'enum': [0,1]},
                        {'description': 'race_Other', 'enum': [0,1]},
                        {'description': 'race_White', 'enum': [0,1]},
                        {'description': 'sex_Female', 'enum': [0,1]},
                        {'description': 'sex_Male', 'enum': [0,1]},
                        {'description': 'native-country_Cambodia', 'enum': [0,1]},
                        {'description': 'native-country_Canada', 'enum': [0,1]},
                        {'description': 'native-country_China', 'enum': [0,1]},
                        {'description': 'native-country_Columbia', 'enum': [0,1]},
                        {'description': 'native-country_Cuba', 'enum': [0,1]},
                        {'description': 'native-country_Dominican-Republic', 'enum': [0,1]},
                        {'description': 'native-country_Ecuador', 'enum': [0,1]},
                        {'description': 'native-country_El-Salvador', 'enum': [0,1]},
                        {'description': 'native-country_England', 'enum': [0,1]},
                        {'description': 'native-country_France', 'enum': [0,1]},
                        {'description': 'native-country_Germany', 'enum': [0,1]},
                        {'description': 'native-country_Greece', 'enum': [0,1]},
                        {'description': 'native-country_Guatemala', 'enum': [0,1]},
                        {'description': 'native-country_Haiti', 'enum': [0,1]},
                        {'description': 'native-country_Holand-Netherlands', 'enum': [0,1]},
                        {'description': 'native-country_Honduras', 'enum': [0,1]},
                        {'description': 'native-country_Hong', 'enum': [0,1]},
                        {'description': 'native-country_Hungary', 'enum': [0,1]},
                        {'description': 'native-country_India', 'enum': [0,1]},
                        {'description': 'native-country_Iran', 'enum': [0,1]},
                        {'description': 'native-country_Ireland', 'enum': [0,1]},
                        {'description': 'native-country_Italy', 'enum': [0,1]},
                        {'description': 'native-country_Jamaica', 'enum': [0,1]},
                        {'description': 'native-country_Japan', 'enum': [0,1]},
                        {'description': 'native-country_Laos', 'enum': [0,1]},
                        {'description': 'native-country_Mexico', 'enum': [0,1]},
                        {'description': 'native-country_Nicaragua', 'enum': [0,1]},
                        {'description': 'native-country_Outlying-US(Guam-USVI-etc)', 'enum': [0,1]},
                        {'description': 'native-country_Peru', 'enum': [0,1]},
                        {'description': 'native-country_Philippines', 'enum': [0,1]},
                        {'description': 'native-country_Poland', 'enum': [0,1]},
                        {'description': 'native-country_Portugal', 'enum': [0,1]},
                        {'description': 'native-country_Puerto-Rico', 'enum': [0,1]},
                        {'description': 'native-country_Scotland', 'enum': [0,1]},
                        {'description': 'native-country_South', 'enum': [0,1]},
                        {'description': 'native-country_Taiwan', 'enum': [0,1]},
                        {'description': 'native-country_Thailand', 'enum': [0,1]},
                        {'description': 'native-country_Trinadad&Tobago', 'enum': [0,1]},
                        {'description': 'native-country_United-States', 'enum': [0,1]},
                        {'description': 'native-country_Vietnam', 'enum': [0,1]},
                        {'description': 'native-country_Yugoslavia', 'enum': [0,1]},
                        {'description': 'age', 'type': 'number'},
                        {'description': 'fnlwgt', 'type': 'number'},
                        {'description': 'education-num', 'type': 'number'},
                        {'description': 'capital-gain', 'type': 'number'},
                        {'description': 'capital-loss', 'type': 'number'},
                        {'description': 'hours-per-week', 'type': 'number'}]}},
            'y': {
                'type': 'array',
                'minItems': 32724, 'maxItems': 32724,
                'items': {'description': 'class', 'enum': [0, 1]}}}}

    covtype_schema = {
        '$schema': 'http://json-schema.org/draft-04/schema#',
        'documentation_url': 'https://scikit-learn.org/0.20/datasets/index.html#forest-covertypes',
        'type': 'object',
        'additionalProperties': False,
        'required': ['X', 'y'],
        'properties': {
            'X': {
                'type': 'array',
                'items': {
                    'type': 'array',
                    'minItems': 54,
                    'maxItems': 54,
                    'items': [
                        {'description': 'Elevation', 'type': 'integer'},
                        {'description': 'Aspect', 'type': 'integer'},
                        {'description': 'Slope', 'type': 'integer'},
                        {'description': 'Horizontal_Distance_To_Hydrology', 'type': 'integer'},
                        {'description': 'Vertical_Distance_To_Hydrology', 'type': 'integer'},
                        {'description': 'Horizontal_Distance_To_Roadways', 'type': 'integer'},
                        {'description': 'Hillshade_9am', 'type': 'integer'},
                        {'description': 'Hillshade_Noon', 'type': 'integer'},
                        {'description': 'Hillshade_3pm', 'type': 'integer'},
                        {'description': 'Horizontal_Distance_To_Fire_Points', 'type': 'integer'},
                        {'description': 'Wilderness_Area1', 'enum': [0, 1]},
                        {'description': 'Wilderness_Area2', 'enum': [0, 1]},
                        {'description': 'Wilderness_Area3', 'enum': [0, 1]},
                        {'description': 'Wilderness_Area4', 'enum': [0, 1]},
                        {'description': 'Soil_Type1', 'enum': [0, 1]},
                        {'description': 'Soil_Type2', 'enum': [0, 1]},
                        {'description': 'Soil_Type3', 'enum': [0, 1]},
                        {'description': 'Soil_Type4', 'enum': [0, 1]},
                        {'description': 'Soil_Type5', 'enum': [0, 1]},
                        {'description': 'Soil_Type6', 'enum': [0, 1]},
                        {'description': 'Soil_Type7', 'enum': [0, 1]},
                        {'description': 'Soil_Type8', 'enum': [0, 1]},
                        {'description': 'Soil_Type9', 'enum': [0, 1]},
                        {'description': 'Soil_Type10', 'enum': [0, 1]},
                        {'description': 'Soil_Type11', 'enum': [0, 1]},
                        {'description': 'Soil_Type12', 'enum': [0, 1]},
                        {'description': 'Soil_Type13', 'enum': [0, 1]},
                        {'description': 'Soil_Type14', 'enum': [0, 1]},
                        {'description': 'Soil_Type15', 'enum': [0, 1]},
                        {'description': 'Soil_Type16', 'enum': [0, 1]},
                        {'description': 'Soil_Type17', 'enum': [0, 1]},
                        {'description': 'Soil_Type18', 'enum': [0, 1]},
                        {'description': 'Soil_Type19', 'enum': [0, 1]},
                        {'description': 'Soil_Type20', 'enum': [0, 1]},
                        {'description': 'Soil_Type21', 'enum': [0, 1]},
                        {'description': 'Soil_Type22', 'enum': [0, 1]},
                        {'description': 'Soil_Type23', 'enum': [0, 1]},
                        {'description': 'Soil_Type24', 'enum': [0, 1]},
                        {'description': 'Soil_Type25', 'enum': [0, 1]},
                        {'description': 'Soil_Type26', 'enum': [0, 1]},
                        {'description': 'Soil_Type27', 'enum': [0, 1]},
                        {'description': 'Soil_Type28', 'enum': [0, 1]},
                        {'description': 'Soil_Type29', 'enum': [0, 1]},
                        {'description': 'Soil_Type30', 'enum': [0, 1]},
                        {'description': 'Soil_Type31', 'enum': [0, 1]},
                        {'description': 'Soil_Type32', 'enum': [0, 1]},
                        {'description': 'Soil_Type33', 'enum': [0, 1]},
                        {'description': 'Soil_Type34', 'enum': [0, 1]},
                        {'description': 'Soil_Type35', 'enum': [0, 1]},
                        {'description': 'Soil_Type36', 'enum': [0, 1]},
                        {'description': 'Soil_Type37', 'enum': [0, 1]},
                        {'description': 'Soil_Type38', 'enum': [0, 1]},
                        {'description': 'Soil_Type39', 'enum': [0, 1]},
                        {'description': 'Soil_Type40', 'enum': [0, 1]}]}},
            'y': {
                'type': 'array',
                'items': {
                    'description': 'The cover type, i.e., the dominant species of trees.',
                    'enum': ['spruce_fir', 'lodgepole_pine', 'ponderosa_pine', 'cottonwood_willow', 'aspen', 'douglas_fir', 'krummholz']}}}}

    operator_names = ['lrOld', 'lrNew', 'project', 'nmf', 'tfidf']
    dataset_names = ['irisArr', 'irisDf', 'digits', 'housing', 'creditG',
                     'movies', 'drugRev', 'adultCat', 'adultNum', 'covtype']

    expected = {
        'lrOld': {
            'irisArr': True, 'irisDf': True, 'digits': True, 'housing': True,
            'creditG': False, 'movies': False, 'drugRev': False,
            'adultCat': False, 'adultNum': True, 'covtype': False},
        'lrNew': {
            'irisArr': True, 'irisDf': True, 'digits': True, 'housing': True,
            'creditG': False, 'movies': False, 'drugRev': False,
            'adultCat': False, 'adultNum': True, 'covtype': True},
        'project': {
            'irisArr': True, 'irisDf': True, 'digits': True, 'housing': True,
            'creditG': True, 'movies': False, 'drugRev': True,
            'adultCat': True, 'adultNum': True, 'covtype': True},
        'nmf': {
            'irisArr': False, 'irisDf': False, 'digits': True, 'housing': False,
            'creditG': False, 'movies': False, 'drugRev': False,
            'adultCat': False, 'adultNum': False, 'covtype': False},
        'tfidf': {
            'irisArr': False, 'irisDf': False, 'digits': False, 'housing': False,
            'creditG': False, 'movies': True, 'drugRev': False,
            'adultCat': False, 'adultNum': False, 'covtype': False}}

    def test_dataset_op(self):
        # for name in  TestAIExamples.operator_names +  TestAIExamples.dataset_names:
        #     schema = self.__getattribute__(name + '_schema')
        #     with open("test/lale/"+name+".json", "w") as f:
        #         f.write(json.dumps(schema))
        count = 0
        for op_name in TestAIExamples.operator_names:
            for ds_name in TestAIExamples.dataset_names:
                op_schema = self.__getattribute__(op_name + '_schema')
                ds_schema = self.__getattribute__(ds_name + '_schema')
                # try:
                result = jsonsubschema.isSubschema(ds_schema, op_schema)
                # result = jsonsubschema.isSubschema(ds_schema, op_schema)
                # assert result == expected[op_name][ds_name], f'dataset {ds_name} operator {op_name}'
                with self.subTest(f'dataset {ds_name} operator {op_name}'):
                    self.assertTrue(result == TestAIExamples.expected[op_name][ds_name])
                    count += 1
                # except Exception:
                #     pass
        print(count)
        
    # def _test_dataset_op_issubset(self):
    #     # for name in  TestAIExamples.operator_names +  TestAIExamples.dataset_names:
    #     #     schema = self.__getattribute__(name + '_schema')
    #     #     with open("test/lale/"+name+".json", "w") as f:
    #     #         f.write(json.dumps(schema))
    #     tp, fp, tn, fn = 0, 0, 0, 0
    #     for j, op_name in enumerate(TestAIExamples.operator_names):
    #         for i, ds_name in enumerate(TestAIExamples.dataset_names):
    #             op_file = "test/lale/"+op_name+".json"
    #             ds_file = "test/lale/"+ds_name+".json"
                
    #             # op_schema = json.load(open(op_file, "r"))
    #             # ds_schema = json.load(open(ds_file, "r"))
    #             # result = jsonsubschema.isSubschema(ds_schema, op_schema)
                
    #             # assert result == expected[op_name][ds_name], f'dataset {ds_name} operator {op_name}'
    #             with self.subTest(f'dataset {ds_name} operator {op_name}: {i,j}'):
    #                 result = run_issubset(ds_file, op_file)
    #                 if result is True:
    #                     if  result != TestAIExamples.expected[op_name][ds_name]:
    #                         fp+=1
    #                     else:
    #                         tp+=1
    #                 elif result is False:
    #                     if result != TestAIExamples.expected[op_name][ds_name]:
    #                         fn+=1
    #                     else:
    #                         tn+= 1
    #                 self.assertTrue(result == TestAIExamples.expected[op_name][ds_name])

    #     print("False positives", fp)
    #     print("False negatives", fn)
    #     print("True positives", tp)
    #     print("True negatives", tn)
