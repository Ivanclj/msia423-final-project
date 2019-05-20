import logging
import argparse
import yaml
import os
import subprocess
import re
import datetime

import pickle

import sklearn
import pandas as pd
import numpy as np

from load_data import load_data
from generate_features import choose_features, get_target
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

    if "choose_features" in kwargs:
        X = choose_features(df, **kwargs["choose_features"])
    else:
        X = df

    # get probability of churn
    y_pred_prob = model.predict_proba(X)[:,1]
    y_predicted = pd.DataFrame(y_pred_prob)
    y_predicted.columns = ['pred_prob']

    # assign class label based on threshold
    y_predicted[y_predicted['pred_prob'] > threshold]['pred'] = 1
    y_predicted[y_predicted['pred_prob'] <= threshold]['pred'] = 0
    
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Score model")
    parser.add_argument('--config', '-c', help='path to yaml file with configurations')
    parser.add_argument('--input', '-i', default=None, help="Path to CSV for input to model scoring")
    parser.add_argument('--output', '-o', default=None, help='Path to where the scores should be saved to (optional)')

    args = parser.parse_args()

    run_scoring(args)