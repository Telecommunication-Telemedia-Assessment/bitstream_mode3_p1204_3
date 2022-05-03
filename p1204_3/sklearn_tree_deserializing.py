#!/usr/bin/env python3
"""
read a json serialized rf model

Steve Göring


the following code is based on https://github.com/mlrequest/sklearn-json/blob/master/sklearn_json/regression.py
however some adjustments were required to make it work with never scikit-learn versions
"""
import inspect
import json

import numpy as np
from sklearn.tree._tree import Tree
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor



def deserialize_tree(tree_dict, n_features, n_classes, n_outputs):
    tree_dict['nodes'] = [tuple(lst) for lst in tree_dict['nodes']]

    names = ['left_child', 'right_child', 'feature', 'threshold', 'impurity', 'n_node_samples', 'weighted_n_node_samples']
    tree_dict['nodes'] = np.array(tree_dict['nodes'], dtype=np.dtype({'names': names, 'formats': tree_dict['nodes_dtype']}))
    tree_dict['values'] = np.array(tree_dict['values'])

    tree = Tree(n_features, np.array([n_classes], dtype=np.intp), n_outputs)
    tree.__setstate__(tree_dict)

    return tree


def deserialize_decision_tree_regressor(model_dict):
    deserialized_decision_tree = DecisionTreeRegressor()

    deserialized_decision_tree.max_features_ = model_dict['max_features_']
    deserialized_decision_tree.n_features_in_ = model_dict['n_features_']
    deserialized_decision_tree.n_outputs_ = model_dict['n_outputs_']

    tree = deserialize_tree(model_dict['tree_'], model_dict['n_features_'], 1, model_dict['n_outputs_'])
    deserialized_decision_tree.tree_ = tree

    return deserialized_decision_tree


def deserialize_random_forest_regressor_json(model_filename_with_path):
    with open(model_filename_with_path) as fp:
        model_dict = json.load(fp)

    # get all params from the RandomForestRegressor constructor
    valid_params = [x.name for x in inspect.signature(RandomForestRegressor).parameters.values()]
    # use only valid params for model creation
    model_dict['params'] = {
        x: model_dict['params'][x]
        for x in set(valid_params) & set(model_dict['params'].keys())
    }

    model = RandomForestRegressor(**model_dict['params'])
    estimators = [deserialize_decision_tree_regressor(decision_tree) for decision_tree in model_dict['estimators_']]
    model.estimators_ = np.array(estimators)

    model.n_features_in_ = model_dict.get('n_features_in_', model_dict["n_features_"])
    model.n_outputs_ = model_dict['n_outputs_']
    model.max_depth = model_dict['max_depth']
    model.min_samples_split = model_dict['min_samples_split']
    model.min_samples_leaf = model_dict['min_samples_leaf']
    model.min_weight_fraction_leaf = model_dict['min_weight_fraction_leaf']
    model.max_features = model_dict['max_features']
    model.max_leaf_nodes = model_dict['max_leaf_nodes']
    model.min_impurity_decrease = model_dict['min_impurity_decrease']
    model.min_impurity_split = model_dict['min_impurity_split']

    if 'oob_score_' in model_dict:
        model.oob_score_ = model_dict['oob_score_']
    if 'oob_prediction_' in model_dict:
        model.oob_prediction_ =np.array(model_dict['oob_prediction_'])

    return model