import pickle
import traceback
import os
#import xgboost
import pandas as pd
from flask import render_template, request, redirect, url_for
import logging.config
#from app import db, app
from flask import Flask
#from src.models import Churn_Prediction
from flask_sqlalchemy import SQLAlchemy


# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from config.py
app.config.from_object('config')

# Define LOGGING_CONFIG in config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
#logging.config.fileConfig(app.config["LOGGING_CONFIG"])
#logger = logging.getLogger("churn-predictor")
#logger.debug('Test log')

# Initialize the database
#db = SQLAlchemy(app)


@app.route('/')
def index():
    """Homepage of this prediction system.
    
    Returns: rendered html template
    """

    try:
        return render_template('index.html')
    except:
        #logger.warning("Not able to display homepage, error page returned")
        return render_template('error.html')

