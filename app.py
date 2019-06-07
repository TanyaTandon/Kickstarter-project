import pickle
import traceback
import os
import xgboost
import pandas as pd
from flask import render_template, request, redirect, url_for
import logging.config
from app import db, app
from flask import Flask
from src.models import Churn_Prediction
from flask_sqlalchemy import SQLAlchemy


# Initialize the Flask application
app = Flask(__name__)

# Configure flask app from config.py
app.config.from_object('config')

# Define LOGGING_CONFIG in config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("churn-predictor")
logger.debug('Test log')

# Initialize the database
db = SQLAlchemy(app)


@app.route('/')
def index():
    """Homepage of this prediction system.
    
    Returns: rendered html template
    """

    try:
        return render_template('homepage.html')
    except:
        logger.warning("Not able to display homepage, error page returned")
        return render_template('error.html')

@app.route('/navigate', methods=['POST','GET'])
def navigate():
    """Main view that get customer information for evaluation.
    Create view into evaluation page that allows to input customer information
    and inserts it into the templates/index.html template.
    
    Returns: rendered html template
    """

    try:
       # redirect to choose threshold page
       return render_template('index.html')
    except:
       logger.warning("Not able to enter customer information, error page returned")
       return render_template('error.html')


@app.route('/list', methods=['POST','GET'])
def list():
    """Main view that get user's choice of threshold for classification.
    Create view into threshold deciding page that determines which customers to be listed in
    later steps and inserts it into the templates/choose_thre.html template.
    
    Returns: rendered html template
    """

    try:
       # redirect to choose threshold page
       return render_template('choose_thre.html')
    except:
       logger.warning("Not able to choose threshold, error page returned")
       return render_template('error.html')


@app.route('/choose_thre', methods=['POST','GET'])
def choose_thre():
    """Main view that lists customers most likely to churn in the database.
    Create view into customer list page that uses data queried from Churn_Prediction database and
    inserts it into the templates/customer_list.html template.
    
    Returns: rendered html template and user's chosen threshold probability level.
    """

    try:
       # get user's choice of threshold - returned type str
       threshold = request.form['threshold']
       # pull customers from database
       customers = db.session.query(Churn_Prediction).limit(app.config["MAX_ROWS_SHOW"]).all()
       logger.debug("customer list page accessed")
       return render_template('customer_list.html', customers=customers, threshold=float(threshold))
    except:
       traceback.print_exc()
       logger.warning("Not able to display customers, error page returned")
       return render_template('error.html')


@app.route('/add', methods=['POST','GET'])
def add_entry():
    """View that process a POST with new customer input
    Returns: rendered html template with evaluation results.
    """

    try:
        # retrieve features
        logger.info("Begining to retrieving")
        Name = request.form['Name']
        Country = request.form['Country']
        Main_Category = request.form['Main_Category']
        Category = request.form['Category']
        Date_Started = request.form['Date_Started']
        Date_Ended = request.form['Date_Ended']
        Goal = request.form['Goal']
        
        logger.info("Successfully retrieved all inputs ")

        # load trained model
        path_to_tmo = app.config["PATH_TO_MODEL"]
        with open(path_to_tmo, "rb") as f:
            model = pickle.load(f)
        logger.info("model loaded!")

        # create a dataframe to store inputs for prediction
        campaign_success = pd.DataFrame(columns=["Name", "Country", "Main_Category", "Category", "Date_Started",
                        "Date_Ended", "Goal"])
        
        campaign_success.loc[0] = [Name, Country, Main_Category, Category, Date_Started,
                           Date_Ended, Goal]

        # change datatype from object to float
        campaign_success = campaign_success.astype("float")
        # make a prediction 
        prob = model.predict_proba(campaign_success)[:,1][0]
        logger.info("prediction made: {:0.3f}".format(prob))

        if prob >= 0.8:
            evaluation = "You are getting the money!!! Hype up and start sprinting work on your dream project. "
        elif prob >= 0.5 and prob < 0.8:
            evaluation = "It's possible your campaign is a hit. But I am not sure  "
        elif prob >= 0.2 and prob < 0.5:
            evaluation = "Pretty difficult"
        else:
            evaluation = "bad news"

        customer1 = Churn_Prediction(Name=String(Name), activeMember=float(Date_Ended), numProducts=float(Category),
            fromGermany=float(Germany), gender=float(Male), Main_Category=float(Main_Category), Date_Started=float(Date_Started),
            Country=float(Country), predicted_score=float(prob))
        db.session.add(customer1)
        db.session.commit()

        logger.info("New customer evaluated as: %s", evaluation)
        
        result = "This customer will churn with probability {:0.3f} - classified as {}".format(prob, evaluation)
        #return redirect(url_for('index'))
        return render_template('index.html', result=result)
    except:
        traceback.print_exc()
        logger.warning("Not able to display evaluations, error page returned")
        return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])

