"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

To understand different arguments, run `python run.py --help`

Current commands enabled:

To create a database for Tracks with an initial song:

    `python run.py create --artist="Britney Spears" --title="Radar" --album="Circus"`

To add a song to an already created database:

    `python run.py ingest --artist="Britney Spears" --title="Radar" --album="Circus"`
"""

import argparse
import logging.config
from app import app
#from app.app import app

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("run-penny-lane")
logger.debug('Test log')

from src.add_songs import create_db, add_track

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create database")
    sb_create.add_argument("--Age", default=33, help="Artist of song to be added")
    sb_create.add_argument("--IsActiveMember", default=1, help="Title of song to be added")
    sb_create.add_argument("--NumOfProducts", default=2, help="Album of song being added.")
    sb_create.add_argument("--Germany", default=0, help="Artist of song to be added")
    sb_create.add_argument("--Male", default=0, help="Title of song to be added")
    sb_create.add_argument("--Balance", default=1000.25, help="Album of song being added.")
    sb_create.add_argument("--HasCrCard", default=0, help="Artist of song to be added")
    sb_create.add_argument("--Tenure", default=2, help="Title of song to be added")
    sb_create.add_argument("--Score", default="prob 0.589", help="Title of song to be added")
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    #sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    #sb_ingest.add_argument("--artist", default="Emancipator", help="Artist of song to be added")
    #sb_ingest.add_argument("--title", default="Minor Cause", help="Title of song to be added")
    #sb_ingest.add_argument("--album", default="Dusk to Dawn", help="Album of song being added")
    #sb_ingest.set_defaults(func=add_track)

    args = parser.parse_args()
    args.func(args)