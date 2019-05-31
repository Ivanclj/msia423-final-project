"""
Created on 5/12/19

@author: Tian Fu

"""
import os
import sys
import logging
import pandas as pd

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql

import argparse


logging.basicConfig(level=logging.DEBUG, filename="logfile_db.log", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger(__file__)


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

    predicted_score = Column(Float, unique=False, nullable=False)



def get_engine_string(RDS = False, conn_type="mysql+pymysql", DATABASE_NAME='msia423'):
    """Get database engine path.

    Args:
        RDS (bool): Whether to create a db locally or on RDS.
        conn_tyep (str): Name of sql connection.
        DATABASE_NAME (str): Name of the database to be used.

    Returns:
        engine_string (str): String defining SQLAlchemy connection URI.

    """
    
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    
    engine_string = "{}://{}:{}@{}:{}/{}". \
        format(conn_type, user, password, host, port, DATABASE_NAME)

    logging.debug("engine string: %s"%engine_string)
    return  engine_string 


def create_db(args,engine=None):
    """Creates a database with the data models inherited from `Base`.

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if engine is None:
        if args.RDS:
            engine_string = get_engine_string()
        else:
            engine_string = args.local_URI
        logger.info("RDS:%s"%args.RDS)
        engine = sql.create_engine(engine_string)

    Base.metadata.create_all(engine)
    logging.info("database created") 

    return engine


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--RDS", default=False, action="store_true", help="True if want to create in RDS else None")
    parser.add_argument("--local_URI", default='sqlite:///../data/database/churn_prediction.db')
    args = parser.parse_args()
    
    engine = create_db(args)


    # create a db session
    Session = sessionmaker(bind=engine)  
    session = Session()
    # add precalculated users and scores
    first_user = Churn_Prediction(age=50,activeMember=1,numProducts=3,fromGermany=1,
        gender=1,balance=70000,hasCrCard=1,tenure=10,predicted_score=0.90703)
    session.add(first_user)
    session.commit()

    second_user = Churn_Prediction(age=32,activeMember=0,numProducts=2,fromGermany=1,
        gender=1,balance=96709.07,hasCrCard=0,tenure=3,predicted_score=0.04434)
    session.add(second_user)
    session.commit()

    third_user = Churn_Prediction(age=57,activeMember=1,numProducts=3,fromGermany=0,
        gender=0,balance=0.0,hasCrCard=1,tenure=9,predicted_score=0.95043)
    session.add(third_user)
    session.commit()

    fourth_user = Churn_Prediction(age=22,activeMember=1,numProducts=1,fromGermany=0,
        gender=0,balance=200.0,hasCrCard=1,tenure=0.7,predicted_score=0.15419)
    session.add(fourth_user)
    session.commit()

    fifth_user = Churn_Prediction(age=80,activeMember=1,numProducts=1,fromGermany=0,
        gender=0,balance=30000.0,hasCrCard=1,tenure=12.0,predicted_score=0.02806)
    session.add(fifth_user)
    session.commit()

    logger.info("Data added")

    query = "SELECT * FROM churn_prediction"
    df = pd.read_sql(query, con=engine)
    logger.info(df)
    session.close()

