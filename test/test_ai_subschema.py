
import numpy
import unittest
import json

import jsonsubschema
from jsonsubschema.exp_dircmp import run_issubset

class TestAIExamples(unittest.TestCase):

    lr_schema = {
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

    operator_names = ['lr', 'project', 'nmf', 'tfidf']
    dataset_names = ['irisArr', 'irisDf', 'digits', 'housing', 'creditG', 'movies', 'drugRev']

    expected = {
        'lr': {
            'irisArr': True, 'irisDf': True, 'digits': True, 'housing': True,
            'creditG': False, 'movies': False, 'drugRev': False},
        'project': {
            'irisArr': True, 'irisDf': True, 'digits': True, 'housing': True,
            'creditG': True, 'movies': False, 'drugRev': True},
        'nmf': {
            'irisArr': False, 'irisDf': False, 'digits': True, 'housing': False,
            'creditG': False, 'movies': False, 'drugRev': False},
        'tfidf': {
            'irisArr': False, 'irisDf': False, 'digits': False, 'housing': False,
            'creditG': False, 'movies': True, 'drugRev': False}}

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