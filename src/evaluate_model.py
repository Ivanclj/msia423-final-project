import logging
import argparse
import yaml
import os
import subprocess
import re
import datetime

import sklearn
import pandas as pd
import numpy as np

from sklearn.metrics import confusion_matrix,classification_report,accuracy_score,roc_auc_score,f1_score

logger = logging.getLogger(__name__)


def evaluate_model(label_df, y_predicted, **kwargs):
    """Evaluate the performance of the model   
    Args:
        label_df (:py:class:`pandas.DataFrame`): Dataframe containing true y label
        y_predicted (:py:class:`pandas.DataFrame`): Dataframe containing predicted probability and score
    Returns: 
        confusion_df (:py:class:`pandas.DataFrame`): Dataframe reporting confusion matrix
    """
    # get predicted scores
    y_pred_prob = y_predicted.iloc[:,0]
    y_pred = y_predicted.iloc[:,1]
    # get true labels
    y_true = label_df.iloc[:,0]

    # calculate auc and accuracy and f1_score if specified
    if "auc" in kwargs["metrics"]:
        auc = roc_auc_score(label_df, y_pred_prob)
        print('AUC on test: %0.3f' % auc)
    if "accuracy" in kwargs["metrics"]:
        accuracy = accuracy_score(label_df, y_pred)
        print('Accuracy on test: %0.3f' % accuracy)
    if "f1_score" in kwargs["metrics"]:
        f1 = f1_score(label_df, y_pred)
        print('F1-score on test: %0.3f' % f1)

    # generate confusion matrix and classification report
    print(classification_report(label_df, y_pred))
    confusion = confusion_matrix(label_df, y_pred)
    print(confusion)
    confusion_df = pd.DataFrame(confusion,
        index=['Actual Negative','Actual Positive'],
        columns=['Predicted Negative', 'Predicted Positive'])
    
    return confusion_df


def run_evaluation(args):
    """Orchestrates the evaluation of the model."""

    with open(args.config, "r") as f:
        config = yaml.load(f)

    if args.input is not None:
        label_df = pd.read_csv(args.input)
    elif "train_model" in config and "split_data" in config["train_model"] and "save_split_prefix" in config["train_model"]["split_data"]:
        label_df = pd.read_csv(config["train_model"]["split_data"]["save_split_prefix"]+ "-test-targets.csv")
        logger.info("test target loaded")
    else:
        raise ValueError("Path to CSV for input data must be provided through --input or "
                         "'train_model' configuration must exist in config file")

    if "score_model" in config and "save_scores" in config["score_model"]:
        score_df = pd.read_csv(config["score_model"]["save_scores"])
        logger.info("Predicted score on test set loaded")
    else:
        raise ValueError("'score_model' configuration mush exist in config file")

    confusion_df = evaluate_model(label_df, score_df, **config["evaluate_model"])
    if args.output is not None:
        confusion_df.to_csv(args.output)
        logger.info("Model evaluation saved to %s", args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Evaluate model")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--input', default=None, help="Path to CSV for input to model scoring")
    parser.add_argument('--output', default=None, help="Path to CSV for output to confusion matrix")

    args = parser.parse_args()

    run_evaluation(args)
