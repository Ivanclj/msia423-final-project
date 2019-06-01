import sys
import os
import json
import warnings
warnings.filterwarnings('ignore')

# for appending dates to filenames
import datetime
import requests
import numpy as np
import logging
import re
import requests
import argparse
import glob
import yaml
import pandas as pd

logger = logging.getLogger(__name__)


def load_csv(path_to_data, columns):
    """Function to get data as a dataframe from an online source.
    Args:
        path_to_data (str): Location where the csv file is saved.
        columns (:obj:`list`): List of features to extract.

    Returns:
        df (:py:class:`pandas.DataFrame`): DataFrame containing extracted features and target.
    """
    
    # load data
    df = pd.read_csv(path_to_data)

    return df[columns]

def load_s3(sourceurl, file_location, columns):
    """Function to get data as a dataframe from an online source.
    Args:
        sourceurl (str): URL of raw data in s3.
        file_location (str): Location where the csv file is saved.
        columns (:obj:`list`): List of features to extract.

    Returns:
        df (:py:class:`pandas.DataFrame`): DataFrame containing extracted features and target.
    """
    try:
        r = requests.get(sourceurl)
        logger.info("Download from s3 bucket.")
        open(file_location, 'wb').write(r.content)
    except requests.exceptions.RequestException:
        logger.error("Error: Unable to download file.")

    # load data
    df = pd.read_csv(file_location)

    return df[columns]


def load_data(config):
    """Function to get data as a dataframe from a csv file.
    Returns:
        df (:py:class:`pandas.DataFrame`): DataFrame containing features and labels.
    """

    how = config["how"].lower()

    if how == "load_csv":
        if "load_csv" not in config:
            raise ValueError("'how' given as 'load_csv' but 'load_csv' not in configuration")
        else:
            df = load_csv(**config["load_csv"]) # load dataframe with all columns selected
    elif how == "load_s3":
        if "load_s3" not in config:
            raise ValueError("'how' given as 'load_s3' but 'load_s3' not in configuration")
        else:
            df = load_s3(**config["load_s3"]) # load dataframe with all columns selected
    else:
        raise ValueError("Option for 'how' is 'load_csv' but %s was given" % how)
    
    # save data
    if "save_data" in config and config["save_data"] is not None:
        df.to_csv(config["save_data"],index=False)
    else:
        raise ValueError("'save_data' need to specify a path")
    
    return df


def run_loading(args):
    """Loads config and executes load data set
    Args:
        args: From argparse, should contain args.config and optionally, args.save
            args.config (str): Path to yaml file with load_data as a top level key containing relevant configurations
            args.save (str): Optional. If given, resulting dataframe will be saved to this location.
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    df = load_data(**config["load_data"])

    if args.save is not None:
        df.to_csv(args.save, index=False)


