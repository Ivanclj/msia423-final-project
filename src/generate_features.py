import logging
import argparse
import yaml
import os
import subprocess
import re
import pandas as pd
import numpy as np

from load_data import load_data

logger = logging.getLogger(__name__)


def choose_features(df, features_to_use=None, target=None, **kwargs):
    """Reduces the dataset to the features_to_use. Will keep the target if provided.
    Args:
        df (:py:class:`pandas.DataFrame`): DataFrame containing the features.
        features_to_use (:obj:`list`): List of columnms to extract from the dataset to be features.
        target (str, optional): If given, will include the target column in the output dataset as well.
    Returns:
        X (:py:class:`pandas.DataFrame`): DataFrame containing extracted features (and target, it applicable).
    """

    logger.debug("Choosing features")
    if features_to_use is not None:
        features = []
        dropped_columns = []
        for column in df.columns:
            # Identifies if this column is in the features to use or if it is a dummy of one of the features to use
            if column in features_to_use or column.split("_dummy_")[0] in features_to_use or column == target:
                features.append(column)
            else:
                dropped_columns.append(column)

        if len(dropped_columns) > 0:
            logger.info("The following columns were not used as features: %s", ",".join(dropped_columns))
        logger.debug(features)
        X = df[features]
    else:
        logger.debug("features_to_use is None, df being returned")
        X = df

    return X


def get_target(df, target, **kwargs):
    """Gets values of target labels of the dataframe."""

    y = df[target]

    return y.values


def generate_features(df, save_features=None, **kwargs):
    """Add transformed features into original dataframe.
    Args:
        df (:py:class:`pandas.DataFrame`): DataFrame containing the data to be transformed into features.
        save_features (str, optional): If given, the feature set will be saved to this path.
        **kwargs: Should contain the arguments for each transformation to be performed on the data, `df`.
            This function assumes each kwarg given except "choose_features" and "get_target" are functions in this file
            that should be evaluated.
    Returns:
        df (:py:class:`pandas.DataFrame`): DataFrame containing original features and transformed features.

    """

    choose_features_kwargs = kwargs["choose_features"]
    df = choose_features(df, **choose_features_kwargs)

    # create dummy for Geography and Gender
    Geography = pd.get_dummies(df['Geography'], drop_first=True)
    Gender = pd.get_dummies(df['Gender'], drop_first=True)
    df.drop(['Geography','Gender'],axis=1,inplace=True)
    # new dataframe after encode categorical variables as dummies
    df1 = pd.concat([df,Geography,Gender],axis=1)

    if save_features is not None:
        df1.to_csv(save_features, index=False)

    return df1


def run_features(args):
    """Orchestrates the generating of features from commandline arguments."""
    
    with open(args.config, "r") as f:
        config = yaml.load(f)

    if args.input is not None:
        df = pd.read_csv(args.input)
    elif "load_data" in config:
        df = load_data(config["load_data"])
    else:
        raise ValueError("Path to CSV for input data must be provided through --csv or "
                         "'load_data' configuration must exist in config file")

    df = generate_features(df, **config["generate_features"])

    if args.output is not None:
        df.to_csv(args.output, index=False)
        logger.info("Features saved to %s", args.output)

    return df


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate features")
    parser.add_argument('--config', help='path to yaml file with configurations')
    parser.add_argument('--input', default=None, help="Path to CSV for generating features from")
    parser.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional)')

    args = parser.parse_args()

    run_features(args)