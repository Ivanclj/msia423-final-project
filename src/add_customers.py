import argparse
import logging.config
import yaml
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData, Float
from sqlalchemy.orm import sessionmaker

#from src.helpers.helpers import create_connection, get_session


logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class Churn_Prediction(Base):
    """Create a data model for the database to be set up for capturing customers """

    __tablename__ = 'churn_prediction'

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    #ip = Column(String(20),nullable=True)
    age = Column(Integer, unique=False, nullable=False)
    activeMember = Column(Integer, unique=False, nullable=False)
    numProducts = Column(Integer, unique=False, nullable=False)
    fromGermany = Column(Integer, unique=False, nullable=False)
    gender = Column(Integer, unique=False, nullable=False)
    balance = Column(Float, unique=False, nullable=False)
    hasCrCard = Column(Integer, unique=False, nullable=False)
    tenure = Column(Float, unique=False, nullable=False)

    predicted_score = Column(String(100), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Churn_Prediction %r>' % self.id


# def create_db(args):
#     """Creates a database with the data model given by obj:`apps.models.Track`
#     Args:
#         args: Argparse args - should include args.title, args.artist, args.album
#     Returns: None
#     """

#     engine = create_connection(engine_string=args.engine_string)

#     Base.metadata.create_all(engine)

#     session = get_session(engine=engine)

#     customer = Churn_Prediction(age=args.Age, activeMember=args.IsActiveMember, numProducts=args.NumOfProducts,
#             fromGermany=args.Germany, gender=args.Male, balance=args.Balance, hasCrCard=args.HasCrCard,
#             tenure=args.Tenure, predicted_score=args.evaluation)

#     db.session.add(customer)
#     session.commit()
#     logger.info("Database created with customer added")
#     session.close()


# if __name__ == '__main__':

#     # Add parsers for both creating a database and adding songs to it
#     parser = argparse.ArgumentParser(description="Create and/or add data to database")
#     subparsers = parser.add_subparsers()

#     # Sub-parser for creating a database
#     sb_create = subparsers.add_parser("create", description="Create database")

#     sb_create.add_argument("--Age", default=33, help="Artist of song to be added")
#     sb_create.add_argument("--IsActiveMember", default=1, help="Title of song to be added")
#     sb_create.add_argument("--NumOfProducts", default=2, help="Album of song being added.")
#     sb_create.add_argument("--Germany", default=0, help="Artist of song to be added")
#     sb_create.add_argument("--Male", default=0, help="Title of song to be added")
#     sb_create.add_argument("--Balance", default=1000.25, help="Album of song being added.")
#     sb_create.add_argument("--HasCrCard", default=0, help="Artist of song to be added")
#     sb_create.add_argument("--Tenure", default=2, help="Title of song to be added")
#     sb_create.add_argument("--Score", default="prob 0.589", help="Title of song to be added")

#     sb_create.add_argument("--engine_string", default='sqlite:///data/Churn_Prediction.db',
#                            help="SQLAlchemy connection URI for database")
#     sb_create.set_defaults(func=create_db)

#     args = parser.parse_args()
#     args.func(args)