from app import db
from app.models import Churn_Prediction
import argparse
import logging.config
logger = logging.getLogger(__name__)


def create_db(args):
    """Creates a database with the data model given by obj:`apps.models.Track`

    Args:
        args: Argparse args - should include args.title, args.artist, args.album

    Returns: None

    """

    db.create_all()

    customer = Churn_Prediction(age=args.Age, activeMember=args.IsActiveMember, numProducts=args.NumOfProducts,
            fromGermany=args.Germany, gender=args.Male, balance=args.Balance, hasCrCard=args.HasCrCard,
            tenure=args.Tenure, predicted_score=args.evaluation)
    db.session.add(customer)
    db.session.commit()
    logger.info("Database created with customer evaluated!")


def add_track(args):
    """Seeds an existing database with additional songs.

    Args:
        args: Argparse args - should include args.title, args.artist, args.album

    Returns:None

    """

    customer = Churn_Prediction(age=args.Age, activeMember=args.IsActiveMember, numProducts=args.NumOfProducts,
            fromGermany=args.Germany, gender=args.Male, balance=args.Balance, hasCrCard=args.HasCrCard,
            tenure=args.Tenure, predicted_score=args.Score)
    db.session.add(customer)
    db.session.commit()
    logger.info("Customer added to database!")


if __name__ == '__main__':

    # Add parsers for both creating a database and adding songs to it
    parser = argparse.ArgumentParser(description="Create and/or add data to database")
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





