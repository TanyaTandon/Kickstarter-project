"""
Enables the command line execution of multiple modules within src/
This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.
To understand different arguments, run `python run.py --help`
"""


import os
import argparse
import config.config as config
import logging
import logging.config

# The logging configurations are called from local.conf
logging.config.fileConfig(os.path.join("config","logging_local.conf"))
logger = logging.getLogger(config.LOGGER_NAME)

from src.load_data import run_loading
from src.model import create_sqlite_db, create_rds_db
from config.config import SQLALCHEMY_DATABASE_URI, DATABASE_NAME

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Data processes")
    subparsers = parser.add_subparsers()

    sub_process = subparsers.add_parser('loadS3')
    sub_process.add_argument("--where", type=str, default="Local", help="'Local' or 'AWS'; The destination bucket name needs to be provided in case of AWS")
    sub_process.add_argument("--bucket", default="None", help="Destination S3 bucket name")
    sub_process.set_defaults(func= run_loading)

    sub_process = subparsers.add_parser('createSqlite')
    sub_process.add_argument("--engine_string", type=str, default=SQLALCHEMY_DATABASE_URI,
                             help="Connection uri for SQLALCHEMY")
    sub_process.set_defaults(func=create_sqlite_db)

    sub_process = subparsers.add_parser('createRDS')
    sub_process.add_argument("--database", type=str, default=DATABASE_NAME,
                             help="Database in RDS")
    sub_process.set_defaults(func=create_rds_db)

    args = parser.parse_args()
    args.func(args)





