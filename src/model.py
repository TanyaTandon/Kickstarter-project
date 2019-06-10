import os
import logging
import logging.config
import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float,  MetaData
from sqlalchemy.ext.declarative import declarative_base
import yaml
import sys
import argparse
import getpass
import pymysql
import sqlalchemy

#sys.path.insert(0, '..')
#from config.config import SQLALCHEMY_DATABASE_URI, DATABASE_NAME


logger = logging.getLogger(__name__)
#logger.setLevel("INFO")

Base = declarative_base()


class Userinput(Base):

    """Creates a database with the data models inherited from `Base` (Usage_Log).
    Args:
        args: Argparse args - include args args.where and args.manual.
    Returns:
        None
    """

    __tablename__ = 'Userinput'

    id = Column(Integer, autoincrement=True, primary_key=True)
    camp_name = Column(String(300), unique=False, nullable=False)
    category = Column(String(100), unique=False, nullable=False)
    launch_day = Column(String(100), unique=False, nullable=False)
    deadline_day = Column(String(100), unique=False, nullable=False)
    goal = Column(Integer, unique=False, nullable=False)
    country = Column(String(100), unique=False, nullable=False)
    

    def __repr__(self):
        Userinput_repr = "<Userinput(id ='%i', camp_name='%s', category='%s', launch_day='%s', deadline_day= '%s', goal= '%i', country= '%s')>"
        return Userinput_repr % (self.id, self.camp_name, self.category, self.launch_day, self.deadline_day, self.goal, self.country)


def create_db(args):
    """Creates a database with the data models inherited from `Base` (Usage_Log).
    Args:
        args: Argparse args - include args args.where and args.manual.
    Returns:
        None
    """
    with open(os.path.join("config","config.yml"), "r") as f:
        config = yaml.safe_load(f)

    logger.debug('Running the create_db function')
    
    if args.where == "Local":
        try:
            logger.info('Creating a local database at {}'.format(config['db_config']['SQLALCHEMY_DATABASE_URI']))
            print((config['db_config']['SQLALCHEMY_DATABASE_URI']))
            engine = sqlalchemy.create_engine(config['db_config']['SQLALCHEMY_DATABASE_URI'])
            logger.debug('Database engine successfully created.')            
        except Exception as e:
            logger.error(e)
            
    elif args.where == "AWS":
        try:
            
            if args.manual == "yes":
                logger.info('Creating an RDS database based on user input.')
                conn_type = "mysql+pymysql"
                user = input("USER:")
                password = getpass.getpass("PASSWORD:")
                host = input("RDS_ENDPOINT:")
                port = input("PORT:")
                db_name = input("DATABASE_NAME:")
                engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, db_name)
            
            else:
                logger.info('Creating an RDS database based on environment variables: MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB.')
                conn_type = "mysql+pymysql"
                user = os.environ.get("MYSQL_USER")
                password = os.environ.get("MYSQL_PASSWORD")
                host = os.environ.get("MYSQL_HOST")
                port = os.environ.get("MYSQL_PORT")
                db_name = os.environ.get("MYSQL_DB")
                engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, db_name)
            
            logger.debug('Creating database now.')    
            engine = create_engine(engine_string)            
            logger.debug('Database engine successfully created.')
        
        except Exception as e:
            logger.error("Database engine cannot be created. Kindly check the configurations and try again.")
            logger.error(e)
    
    else:
        raise ValueError('Kindly check the arguments and rerun. To understand different arguments, run `python run.py --help`')
    
    if args.where in ["AWS", "Local"]:    
        try:
            Base.metadata.create_all(engine)
            logger.info('Database successfully created.')            
    
        except Exception as e:
            logger.error("Database could not be created. Kindly check the configurations and try again.")


