import logging
import argparse
import yaml
import os
import subprocess
import re
import datetime

import pickle

import sklearn
from sklearn.exceptions import NotFittedError
import pandas as pd
import numpy as np

from src.load_data import load_data
from src.generate_features import choose_features, get_target
import xgboost as xgb

logger = logging.getLogger(__name__)

#score_model_kwargs = ["predict"]

def score_model(df, path_to_tmo, threshold, save_scores=None, **kwargs):
    """Get prediction results for the test set.
    Args:
        df (:py:class:`pandas.DataFrame`): Dataframe containing data to run prediction on.
        path_to_tmo (str): Path to trained model.
        threshold (int): classify customer as churned if predicted probability above this threshold.
        save_scores (str): Path to save prediction results. Default to None.
    Returns:
        y_predicted (:py:class:`pandas.DataFrame`): DataFrame containing predicted scores.
    
    """

    with open(path_to_tmo, "rb") as f:
        model = pickle.load(f)

    # check model type - has to be xgboost
    if str(type(model)) != "<class 'xgboost.sklearn.XGBClassifier'>":
        raise TypeError("model used to score must be an XGBoost Classifier")

    if "choose_features" in kwargs:
        X = choose_features(df, **kwargs["choose_features"])
    else:
        X = df
    
    # check if input dataframe for scoring has only numeric or boolean columns
    for col in X.columns:
        if X[col].dtype not in [np.dtype('float64'), np.dtype('float32'), np.dtype('int64'), np.dtype('bool')]:
            raise ValueError('Input dataframe can only have numeric or boolean types!')

    # check if the model loaded has been fitted or not in order to proceed to prediction stage
    try:
        # get probability of churn
        y_pred_prob = model.predict_proba(X)[:,1]
    except:
        raise NotFittedError('Model needs to be fitted before making predictions!')
    y_predicted = pd.DataFrame(y_pred_prob)
    y_predicted.columns = ['pred_prob']
    
    logger.info("chosen threshold is {}".format(threshold))

    # assign class label based on threshold
    def predicted_label(row):
        """helper function for assign predicted labels."""
        if row['pred_prob'] > threshold:
            return 1
        else:
            return 0
    y_predicted['pred'] = y_predicted.apply(lambda row: predicted_label(row), axis=1)

    #y_predicted.loc[y_predicted['pred_prob'] > threshold]['pred'] = 1
    #y_predicted.loc[y_predicted['pred_prob'] <= threshold]['pred'] = 0
    # see if there are two columns
    if len(y_predicted.columns) > 0:
        logger.info("The following columns are included in scores: %s", ",".join(y_predicted.columns))

    # save prediction results
    if save_scores is not None:
        y_predicted.to_csv(save_scores, index=False)

    return y_predicted


def run_scoring(args):
    """Orchestrates the scoring of model."""
    
    with open(args.config, "r") as f:
        config = yaml.load(f)

    if args.input is not None:
        df = pd.read_csv(args.input)
    elif "train_model" in config and "split_data" in config["train_model"] and "save_split_prefix" in config["train_model"]["split_data"]:
        df = pd.read_csv(config["train_model"]["split_data"]["save_split_prefix"]+ "-test-features.csv")
    else:
        raise ValueError("Path to CSV for input data must be provided through --input or "
                         "'load_data' configuration must exist in config file")
    # Get predicted scores of the test set.
    y_predicted = score_model(df, **config["score_model"])

    if args.output is not None:
        pd.DataFrame(y_predicted).to_csv(args.output, index=False)


