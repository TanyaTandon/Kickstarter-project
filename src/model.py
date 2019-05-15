
import argparse
import logging.config
import os
import sys

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, MetaData

sys.path.append(os.path.abspath(os.path.join('..')))

from config import SQLALCHEMY_DATABASE_URI, DATABASE_NAME


logger = logging.getLogger(__name__)
logger.setLevel("INFO")

Base = declarative_base()


class Userinput(Base):

    """Create a data model for the database to be set up for capturing user input

    """

    __tablename__ = 'Userinput'

    id = Column(Integer, primary_key=True)
    camp_name = Column(String(300), unique=False, nullable=False)
    category = Column(String(100), unique=False, nullable=False)
    launch_day = Column(String(100), unique=False, nullable=False)
    deadline_day = Column(String(100), unique=False, nullable=False)
    goal = Column(Integer, unique=False, nullable=False)
    country = Column(String(100), unique=False, nullable=False)
    

    def __repr__(self):
        Userinput_repr = "<Userinput(id= '%i', camp_name='%s', category='%s', launch_day='%s', deadline_day= '%s', goal= '%i', country= '%s')>"
        return Userinput_repr % (self.id, self.camp_name, self.category, self.launch_day, self.deadline_day, self.goal, self.country)


def create_sqlite_db(args):
    """Creates an sqlite database with the data models inherited from `Base` .
    Args:
        args (argument from user): String defining SQLAlchemy connection URI in the form of
    Returns:
        None
    """

    engine = sqlalchemy.create_engine(args.engine_string)
    Base.metadata.create_all(engine)


def create_rds_db(args):
    """Creates an rds table? with the data models inherited from `Base` (UserLines).
        Args:
            args (argument from user): String defining RDS in the desrired form
        Returns:
            None
    """

    conn_type = "mysql+pymysql"
    user = os.environ.get("MYSQL_USER")
    password = os.environ.get("MYSQL_PASSWORD")
    host = os.environ.get("MYSQL_HOST")
    port = os.environ.get("MYSQL_PORT")
    engine_string = "{}://{}:{}@{}:{}/{}". \
        format(conn_type, user, password, host, port, DATABASE_NAME)

    engine = sqlalchemy.create_engine(engine_string)
    Base.metadata.create_all(engine)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('createSqlite')
    sub_process.add_argument("--database", type=str, default=SQLALCHEMY_DATABASE_URI,
                             help="Connection uri for SQLALCHEMY")
    sub_process.set_defaults(func=create_sqlite_db)

    sub_process = subparsers.add_parser('createRDS')
    sub_process.add_argument("--database", type=str, default=DATABASE_NAME,
                             help="Database in RDS")
    sub_process.set_defaults(func=create_rds_db)

    args = parser.parse_args()
    args.func(args)