'''
Created on Aug. 24, 2019
@author: Andrew Habib
'''
import copy
import unittest

from jsonsubschema import isSubschema


class TestMore(unittest.TestCase):

    def test_1(self):
        s1 = {"type": "object", 
                "properties": {"loss": {"enum": ["deviance", "exponential"]}, 
                                "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, 
                                "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, 
                                "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, 
                                "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, 
                                "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, 
                                "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, 
                                "max_features": {"enum": ["auto", "sqrt", "log2", None]}, 
                                "presort": {"enum": ["auto"]}, 
                                "n_iter_no_change": {"enum": [None]}, 
                                "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, 
                "additionalProperties": False, 
                "required": ["presort"]}

        s2 = {"type": "object", 
                "properties": {"loss": {"enum": ["deviance", "exponential"]}, 
                                "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, 
                                "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, 
                                "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, 
                                "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, 
                                "min_samples_leaf": {
                                "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, 
                                "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, 
                                "max_features": {"enum": ["auto", "sqrt", "log2", None]}, 
                                "presort": {"enum": ["auto"]}, 
                                "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, 
                                "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, 
                "additionalProperties": False, 
                "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_2(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_3(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_4(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_5(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_6(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_7(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_8(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_9(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_10(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_11(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_12(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_13(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_14(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_15(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_16(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_17(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_18(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_19(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_20(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_21(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_22(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_23(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_24(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance", "exponential"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_25(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_26(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_27(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_28(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_29(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_30(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_31(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_32(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_33(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_34(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_35(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_36(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_37(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_38(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_39(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_40(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_41(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_42(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_43(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_44(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_45(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_46(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_47(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_48(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["deviance"]}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "subsample": {"default": 1.0, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {
            "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_49(self):
        s1 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf"]}}}}
        s2 = {"type": "object", "properties": {
            "subsample_freq": {"not": {"enum": [0]}}, 
            "subsample": {"not": {"enum": [1.0]}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_50(self):
        s1 = {"type": "object", "properties": {"subsample_freq": {
            "not": {"enum": [0]}}, "subsample": {"not": {"enum": [1.0]}}}}
        s2 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf"]}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_51(self):
        s1 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf", "goss"]}}}}
        s2 = {"type": "object", "properties": {"subsample_freq": {"not": {"enum": [0]}}, "subsample": {
            "not": {"enum": [1.0]}}, "boosting_type": {"not": {"enum": ["goss"]}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
    
    def test_52(self):
        s1 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf", "goss"]}}}}
        s2 = {"type": "object", "properties": {
            "subsample_freq": {"not": {}}, "subsample": {"not": {}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_53(self):
        s1 = {"type": "object", "properties": {
            "subsample_freq": {"not": {"enum": [0]}}, 
            "subsample": {"not": {"enum": [1.0]}}, 
            "boosting_type": {"not": {"enum": ["goss"]}}}}
        s2 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf", "goss"]}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_54(self):
        s1 = {"type": "object", "properties": {"subsample_freq": {"not": {"enum": [0]}}, "subsample": {
            "not": {"enum": [1.0]}}, "boosting_type": {"not": {"enum": ["goss"]}}}}
        s2 = {"type": "object", "properties": {"boosting_type": {"not": {"enum": [
            "rf"]}}, "subsample_freq": {"enum": [0]}, "subsample": {"enum": [1.0]}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_55(self):
        s1 = {"type": "object", "properties": {"subsample_freq": {"not": {"enum": [0]}}, "subsample": {
            "not": {"enum": [1.0]}}, "boosting_type": {"not": {"enum": ["goss"]}}}}
        s2 = {"type": "object", "properties": {
            "subsample_freq": {"not": {}}, "subsample": {"not": {}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_56(self):
        s1 = {"type": "object", "properties": {
            "subsample_freq": {"not": {}}, "subsample": {"not": {}}}}
        s2 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf", "goss"]}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_57(self):
        s1 = {"type": "object", "properties": {
            "subsample_freq": {"not": {}}, "subsample": {"not": {}}}}
        s2 = {"type": "object", "properties": {"boosting_type": {"not": {"enum": [
            "rf"]}}, "subsample_freq": {"enum": [0]}, "subsample": {"enum": [1.0]}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))            

    def test_58(self):
        s1 = {"type": "object", "properties": {
            "subsample_freq": {"not": {}}, "subsample": {"not": {}}}}
        s2 = {"type": "object", "properties": {"subsample_freq": {"not": {"enum": [0]}}, "subsample": {
            "not": {"enum": [1.0]}}, "boosting_type": {"not": {"enum": ["goss"]}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_59(self):
        s1 = {"type": "object", "properties": {"boosting_type": {"enum": ["gbdt", "dart"]}, "max_depth": {"type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 50, "maximumForOptimizer": 500}, "min_child_samples": {
            "default": 20, "type": "integer", "minimumForOptimizer": 1, "maximumForOptimizer": 20}, "subsample": {"default": 1.0, "type": "number", "minimum": 0.0, "exclusiveMinimum": True, "minimumForOptimizer": 0.1, "maximum": 1.0}, "subsample_freq": {"default": 0, "type": "integer", "minimumForOptimizer": 0, "maximumForOptimizer": 10}}, "additionalProperties": False, "required": ["min_child_samples", "max_depth", "n_estimators", "subsample_freq", "boosting_type", "subsample", "learning_rate"]}
        s2 = {"type": "object", "properties": {"boosting_type": {"enum": ["gbdt", "dart", "rf"]}, "max_depth": {"type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 50, "maximumForOptimizer": 500}, "min_child_samples": {"default": 20, "type": "integer", "minimumForOptimizer": 1, "maximumForOptimizer": 20}, "subsample": {
            "default": 1.0, "type": "number", "minimum": 0.0, "exclusiveMinimum": True, "minimumForOptimizer": 0.1, "maximum": 1.0, "exclusiveMaximum": True}, "subsample_freq": {"allOf": [{"default": 0, "type": "integer", "minimumForOptimizer": 0, "exclusiveMinimumForOptimizer": True, "maximumForOptimizer": 10}, {"not": {"enum": [0]}}]}}, "additionalProperties": False, "required": ["min_child_samples", "max_depth", "n_estimators", "subsample_freq", "boosting_type", "subsample", "learning_rate"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_60(self):
        s1 = {"type": "object", "properties": {"boosting_type": {"enum": ["gbdt", "dart", "rf"]}, "max_depth": {"type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 50, "maximumForOptimizer": 500}, "min_child_samples": {"default": 20, "type": "integer", "minimumForOptimizer": 1, "maximumForOptimizer": 20}, "subsample": {
            "default": 1.0, "type": "number", "minimum": 0.0, "exclusiveMinimum": True, "minimumForOptimizer": 0.1, "maximum": 1.0, "exclusiveMaximum": True}, "subsample_freq": {"allOf": [{"default": 0, "type": "integer", "minimumForOptimizer": 0, "exclusiveMinimumForOptimizer": True, "maximumForOptimizer": 10}, {"not": {"enum": [0]}}]}}, "additionalProperties": False, "required": ["min_child_samples", "max_depth", "n_estimators", "subsample_freq", "boosting_type", "subsample", "learning_rate"]}
        s2 = {"type": "object", "properties": {"boosting_type": {"enum": ["gbdt", "dart"]}, "max_depth": {"type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 50, "maximumForOptimizer": 500}, "min_child_samples": {
            "default": 20, "type": "integer", "minimumForOptimizer": 1, "maximumForOptimizer": 20}, "subsample": {"default": 1.0, "type": "number", "minimum": 0.0, "exclusiveMinimum": True, "minimumForOptimizer": 0.1, "maximum": 1.0}, "subsample_freq": {"default": 0, "type": "integer", "minimumForOptimizer": 0, "maximumForOptimizer": 10}}, "additionalProperties": False, "required": ["min_child_samples", "max_depth", "n_estimators", "subsample_freq", "boosting_type", "subsample", "learning_rate"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_61(self):
        s1 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf"]}}}}
        s2 = {"type": "object", "properties": {"subsample_freq": {
            "not": {"enum": [0]}}, "subsample": {"not": {"enum": [1.0]}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_62(self):
        s1 = {"type": "object", "properties": {"subsample_freq": {
            "not": {"enum": [0]}}, "subsample": {"not": {"enum": [1.0]}}}}
        s2 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf"]}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_63(self):
        s1 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf", "goss"]}}}}
        s2 = {"type": "object", "properties": {"subsample_freq": {"not": {"enum": [0]}}, "subsample": {
            "not": {"enum": [1.0]}}, "boosting_type": {"not": {"enum": ["goss"]}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_64(self):
        s1 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf", "goss"]}}}}
        s2 = {"type": "object", "properties": {
            "subsample_freq": {"not": {}}, "subsample": {"not": {}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
    
    def test_65(self):
        s1 = {"type": "object", "properties": {
            "subsample_freq": {"not": {"enum": [0]}}, 
            "subsample": {"not": {"enum": [1.0]}}, 
            "boosting_type": {"not": {"enum": ["goss"]}}}}
        s2 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf", "goss"]}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_66(self):
        s1 = {"type": "object", "properties": {"subsample_freq": {"not": {"enum": [0]}}, "subsample": {
            "not": {"enum": [1.0]}}, "boosting_type": {"not": {"enum": ["goss"]}}}}
        s2 = {"type": "object", "properties": {"boosting_type": {"not": {"enum": [
            "rf"]}}, "subsample_freq": {"enum": [0]}, "subsample": {"enum": [1.0]}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_67(self):
        s1 = {"type": "object", "properties": {"subsample_freq": {"not": {"enum": [0]}}, "subsample": {
            "not": {"enum": [1.0]}}, "boosting_type": {"not": {"enum": ["goss"]}}}}
        s2 = {"type": "object", "properties": {
            "subsample_freq": {"not": {}}, "subsample": {"not": {}}}}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_68(self):
        s1 = {"type": "object", "properties": {
            "subsample_freq": {"not": {}}, "subsample": {"not": {}}}}
        s2 = {"type": "object", "properties": {
            "boosting_type": {"not": {"enum": ["rf", "goss"]}}}}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_69(self):
        s1 = {"type": "object", "properties": {
            "subsample_freq": {"not": {}}, "subsample": {"not": {}}}}
        s2 = {"type": "object", "properties": {"boosting_type": {"not": {"enum": [
            "rf"]}}, "subsample_freq": {"enum": [0]}, "subsample": {"enum": [1.0]}}}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_70(self):
        s1 = {"type": "object", "properties": {
            "subsample_freq": {"not": {}}, "subsample": {"not": {}}}}
        s2 = {"type": "object", "properties": {"subsample_freq": {"not": {"enum": [0]}}, "subsample": {
            "not": {"enum": [1.0]}}, "boosting_type": {"not": {"enum": ["goss"]}}}}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_71(self):
        s1 = {"type": "object", "properties": {"boosting_type": {"enum": ["gbdt", "dart"]}, "max_depth": {"type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 50, "maximumForOptimizer": 500}, "min_child_samples": {
            "default": 20, "type": "integer", "minimumForOptimizer": 1, "maximumForOptimizer": 20}, "subsample": {"default": 1.0, "type": "number", "minimum": 0.0, "exclusiveMinimum": True, "minimumForOptimizer": 0.1, "maximum": 1.0}, "subsample_freq": {"default": 0, "type": "integer", "minimumForOptimizer": 0, "maximumForOptimizer": 10}}, "additionalProperties": False, "required": ["min_child_samples", "max_depth", "n_estimators", "subsample_freq", "boosting_type", "subsample", "learning_rate"]}
        s2 = {"type": "object", "properties": {"boosting_type": {"enum": ["gbdt", "dart", "rf"]}, "max_depth": {"type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 50, "maximumForOptimizer": 500}, "min_child_samples": {"default": 20, "type": "integer", "minimumForOptimizer": 1, "maximumForOptimizer": 20}, "subsample": {
            "default": 1.0, "type": "number", "minimum": 0.0, "exclusiveMinimum": True, "minimumForOptimizer": 0.1, "maximum": 1.0, "exclusiveMaximum": True}, "subsample_freq": {"allOf": [{"default": 0, "type": "integer", "minimumForOptimizer": 0, "exclusiveMinimumForOptimizer": True, "maximumForOptimizer": 10}, {"not": {"enum": [0]}}]}}, "additionalProperties": False, "required": ["min_child_samples", "max_depth", "n_estimators", "subsample_freq", "boosting_type", "subsample", "learning_rate"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_72(self):
        s1 = {"type": "object", "properties": {"boosting_type": {"enum": ["gbdt", "dart", "rf"]}, "max_depth": {"type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 50, "maximumForOptimizer": 500}, "min_child_samples": {"default": 20, "type": "integer", "minimumForOptimizer": 1, "maximumForOptimizer": 20}, "subsample": {
            "default": 1.0, "type": "number", "minimum": 0.0, "exclusiveMinimum": True, "minimumForOptimizer": 0.1, "maximum": 1.0, "exclusiveMaximum": True}, "subsample_freq": {"allOf": [{"default": 0, "type": "integer", "minimumForOptimizer": 0, "exclusiveMinimumForOptimizer": True, "maximumForOptimizer": 10}, {"not": {"enum": [0]}}]}}, "additionalProperties": False, "required": ["min_child_samples", "max_depth", "n_estimators", "subsample_freq", "boosting_type", "subsample", "learning_rate"]}
        s2 = {"type": "object", "properties": {"boosting_type": {"enum": ["gbdt", "dart"]}, "max_depth": {"type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "learning_rate": {"default": 0.1, "type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 1.0}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 50, "maximumForOptimizer": 500}, "min_child_samples": {
            "default": 20, "type": "integer", "minimumForOptimizer": 1, "maximumForOptimizer": 20}, "subsample": {"default": 1.0, "type": "number", "minimum": 0.0, "exclusiveMinimum": True, "minimumForOptimizer": 0.1, "maximum": 1.0}, "subsample_freq": {"default": 0, "type": "integer", "minimumForOptimizer": 0, "maximumForOptimizer": 10}}, "additionalProperties": False, "required": ["min_child_samples", "max_depth", "n_estimators", "subsample_freq", "boosting_type", "subsample", "learning_rate"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_73(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean"]}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_74(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean"]}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_75(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"]}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_76(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"]}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_77(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean"]}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_78(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean"]}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_79(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"]}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_80(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"]}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_81(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean"]}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))


    def test_82(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, 
                                                # "affinity": {"not": {}},
                                                "compute_full_tree": {"enum": ["auto"]}, 
                                                "linkage": {"enum": ["ward", "complete", "average", "single"]}}, 
                                                # },
                                "additionalProperties": False, 
                                "required": ["compute_full_tree"]}

        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, 
                                                # "affinity": {"enum": ["euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"]}, 
                                                "compute_full_tree": {"enum": ["auto"]}, 
                                                "linkage": {"enum": ["complete", "average", "single"]}}, 
                                "additionalProperties": False, 
                                "required": ["compute_full_tree"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_83(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean"]}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_84(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"]}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_85(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"forOptimizer": {"not": {}},
                                                                                                                                                                 "type": "object"}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_86(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_87(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"forOptimizer": False,
                                                                                                                                                                 "type": "object"}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_88(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"forOptimizer": {"not": {}},
                                                                                                                                                                 "type": "object"}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_89(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"forOptimizer": {"not": {}},
                                                                                                                                                                 "type": "object"}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_90(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean"]}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_91(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"]}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_92(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean"]}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))

    def test_93(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"enum": [
            "euclidean", "l1", "l2", "manhattan", "cosine", "precomputed"]}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_94(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_95(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"forOptimizer": {"not": {}},
                                                                                                                                                                 "type": "object"}, "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_96(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"forOptimizer": {"not": {}},
                                                                                                                                                                 "type": "object"}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_97(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"forOptimizer": {"not": {}},
                                                                                                                                                                 "type": "object"}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"enum": ["auto"]}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_98(self):
        s1 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"forOptimizer": {"not": {}},
                                                                                                                                                                 "type": "object"}, "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        s2 = {"type": "object", "properties": {"n_clusters": {"default": 2, "type": "integer", "minimumForOptimizer": 2, "maximumForOptimizer": 8}, "affinity": {"not": {}},
                                               "compute_full_tree": {"type": "boolean"}, "linkage": {"enum": ["ward", "complete", "average", "single"]}}, "additionalProperties": False, "required": ["compute_full_tree"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_99(self):
        s1 = {"type": "object", "properties": {"n_components": {"enum": [None, "mle"]}, "whiten": {"default": False, "type": "boolean"}, "svd_solver": {
            "enum": ["auto", "full"]}}, "additionalProperties": False, "required": ["svd_solver", "n_components", "whiten"]}
        s2 = {"type": "object", "properties": {"n_components": {"enum": [None, "mle"]}, "whiten": {"default": False, "type": "boolean"}, "svd_solver": {
            "enum": ["full"]}}, "additionalProperties": False, "required": ["svd_solver", "n_components", "whiten"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_100(self):
        s1 = {"type": "object", "properties": {
            "n_components": {"enum": [None, "mle"]}, 
            "whiten": {"default": False, "type": "boolean"}, 
            "svd_solver": {"enum": ["full"]}}, 
        "additionalProperties": False, 
        "required": ["svd_solver", "n_components", "whiten"]}
        
        s2 = {"type": "object", "properties": {
            "n_components": {"enum": [None, "mle"]}, 
            "whiten": {"default": False, "type": "boolean"}, 
            "svd_solver": {"enum": ["auto", "full"]}}, 
        "additionalProperties": False, 
        "required": ["svd_solver", "n_components", "whiten"]}
        
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))

    def test_101(self):
        s1 = {"type": "object", "properties": {"n_components": {"enum": [None, "mle"]}, "whiten": {"default": False, "type": "boolean"}, "svd_solver": {
            "enum": ["auto", "full"]}}, "additionalProperties": False, "required": ["svd_solver", "n_components", "whiten"]}
        s2 = {"type": "object", "properties": {"n_components": {"enum": [None, "mle"]}, "whiten": {"default": False, "type": "boolean"}, "svd_solver": {
            "enum": ["full"]}}, "additionalProperties": False, "required": ["svd_solver", "n_components", "whiten"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_102(self):
        s1 = {"type": "object", "properties": {
            "n_components": {"enum": [None, "mle"]}, 
            "whiten": {"default": False, "type": "boolean"}, 
            "svd_solver": {"enum": ["full"]}}, 
        "additionalProperties": False, 
        "required": ["svd_solver", "n_components", "whiten"]}
        
        s2 = {"type": "object", "properties": {
            "n_components": {"enum": [None, "mle"]}, 
            "whiten": {"default": False, "type": "boolean"}, 
            "svd_solver": {"enum": ["auto", "full"]}}, 
        "additionalProperties": False, 
        "required": ["svd_solver", "n_components", "whiten"]}
        
        with self.subTest():
            self.assertTrue(isSubschema(s1, s2))

    def test_103(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_104(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_105(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_106(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_107(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_108(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_109(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_110(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_111(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
            
    def test_112(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
            
    def test_113(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        
        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
    
    def test_114(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_115(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_116(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_117(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_118(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_119(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_120(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_121(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_122(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_123(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_124(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_125(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_126(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_127(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_128(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_129(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {"default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {
            "enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "type": "number", "minimumForOptimizer": 1e-10, "maximumForOptimizer": 1.0}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_130(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_131(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"enum": ["auto"]}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))

    def test_132(self):
        s1 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"type": "integer", "minimumForOptimizer": 5, "maximumForOptimizer": 10}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}
        s2 = {"type": "object", "properties": {"loss": {"enum": ["ls", "lad", "huber", "quantile"]}, "n_estimators": {"default": 100, "type": "integer", "minimumForOptimizer": 10, "maximumForOptimizer": 100}, "min_samples_split": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "min_samples_leaf": {"type": "number", "minimumForOptimizer": 0.01, "maximumForOptimizer": 0.5}, "max_depth": {
            "default": 3, "type": "integer", "minimumForOptimizer": 3, "maximumForOptimizer": 5}, "max_features": {"enum": ["auto", "sqrt", "log2", None]}, "alpha": {"default": 0.9, "enum": [0.9]}, "presort": {"type": "boolean"}, "n_iter_no_change": {"enum": [None]}, "tol": {"default": 0.0001, "type": "number", "minimumForOptimizer": 1e-08, "maximumForOptimizer": 0.01}}, "additionalProperties": False, "required": ["presort"]}

        with self.subTest():
            self.assertFalse(isSubschema(s1, s2))
