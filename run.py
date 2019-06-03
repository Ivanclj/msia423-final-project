"""Enables the command line execution of multiple modules within src/
This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.
To understand different arguments, run `python run.py --help`
"""
import argparse
import logging.config
from app import app

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("churn-predictor")
logger.debug('Test log')

from src.load_data import run_loading
from src.generate_features import run_features
from src.train_model import run_training
from src.score_model import run_scoring
from src.evaluate_model import run_evaluation


def run_app(args):
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    # DATA LOADING subparser
    sb_load = subparsers.add_parser("load_data", description="Load data into a dataframe")
    sb_load.add_argument('--config', help='path to yaml file with configurations')
    sb_load.add_argument('--save', default=None, help='Path to where the dataset should be saved to (optional')
    sb_load.set_defaults(func=run_loading)

    # FEATURE subparser
    sb_features = subparsers.add_parser("generate_features", description="Generate features")
    sb_features.add_argument('--config', help='path to yaml file with configurations')
    sb_features.add_argument('--input', default=None, help="Path to CSV for input to model scoreing")
    sb_features.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    sb_features.set_defaults(func=run_features)

    # TRAIN subparser
    sb_train = subparsers.add_parser("train_model", description="Train model")
    sb_train.add_argument('--config', help='path to yaml file with configurations')
    sb_train.add_argument('--input', default=None, help="Path to CSV for input to model training")
    sb_train.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    sb_train.set_defaults(func=run_training)

    # SCORE subparser
    sb_score = subparsers.add_parser("score_model", description="Score model")
    sb_score.add_argument('--config', help='path to yaml file with configurations')
    sb_score.add_argument('--input', default=None, help="Path to CSV for input to model scoring")
    sb_score.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    sb_score.set_defaults(func=run_scoring)

    # EVALUATION subparser
    sb_eval = subparsers.add_parser("evaluate_model", description="Evaluate model")
    sb_eval.add_argument('--config', help='path to yaml file with configurations')
    sb_eval.add_argument('--input', default=None, help="Path to CSV for input to model evaluation")
    sb_eval.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    sb_eval.set_defaults(func=run_evaluation)
    
    # RUN APP subparser
    sb_run = subparsers.add_parser("app", description="Run Flask app")
    sb_run.set_defaults(func=run_app)

    args = parser.parse_args()
    args.func(args)



