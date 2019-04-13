# Dear Genie

**Vision**: In the history of the world, today is the best time for a dream to come true. With distances in the world shrinking by the internet, Kickstarter is one of the fastest and easiest ways to kickstart a great idea. Theis project aligns with Kickstarters mission to "help bring creative projects to life" by predicting if a kickstarter campaign will be successfull or not.

**Mission**:  Since the goal of the project is to predict success of a Kickstarter project, it will help users evaluate whether their campaign will be able to raise money or not even before they do it. It will further suggest alternate completion dates as well as alternate goals that will be more likely to succeed to help users modify their campaign for a sure shot success. 

**Success criteria**:  
- Accuracy of atleast 60% ( Using AUC or Missclassification rate) 
- Inbound traffic of atleast 100 Kickstarter campaign starters
- Above 70 % positive feedback on UX design

# Planned work 

### Theme 1: Model Development

***Epic 1:*** Design data set that best represents  all aspects needed to classify a Kickstarter project

-  **Story 1:** Sort the relevant as well as connectable dataset from Kaggle
- **Story 2:** Connect all these data sets
- **Story 3:** Design new features

***Epic 2:*** EDA and Data cleaning and preparation for modeling

***Epic 3:*** Initial Model Development

- **Story 1:** Build logistic regression model
- **Story 2:** Build boosted trees
- **Story 3:** Build Random Forest
- **Story 4:** Compare measures of success (AOC, missclass rate, recall, etc) (%) for each on new data 
- **Story 5:** Reiterate the model for improvement

***Epic 4:*** Create unit test scripts to test model functionality 

### Theme2 : App Development 
***Epic 1:*** Setting up the requirements.txt from the current enviornment state to make reproducible environment

***Epic 2:*** Deploy the flask app 

***Epic 3:*** Setup Amazon cloud server for file hosting


***Epic 4:*** Setup front end interface UI where the users will interact with the model built
- **Story1:**  Setup a basic front end interface with all the required options
- **Story 2:**  Improve the baisc front end interface to include engaging gifs on the Home page

***Epic 4:*** Create UAT test scripts to test that UI is working as expected to intake selections and output accordingly
- **Story1:**  Check for model functionality 
- **Story 2:** Check for exception handling by UI 

***Epic 5:***  Create logging for easy debugging and error notifications







# Backlog 
**Sprint Sizing Legend:**

-   0 points - quick chore
-   1 point ~ 1 hour (small)
-   2 point ~ 2.5 hour ( slightly bigger than small) 
-   3 points ~ 1/2 day (medium)
-   4 points ~ 1 day (large)
-   8 points - big and needs to be broken down more when it comes to execution (okay as placeholder for future work though)
    
1.  **Theme1.epic1.story1**  (2pts) - PLANNED: sprint 1
    
2.  **Theme1.epic1.story2**  (2pts) - PLANNED: sprint 1
    
3.  **Theme1.epic1.story3**  (2pts) - PLANNED: sprint 1
    
4.  **Theme1.epic2**  (3pts) - PLANNED: sprint 1
    
5.  **Theme1.epic3.story1**  (2pts)
    
6.  **Theme1.epic3.story2**  (2pts)
    
7.  **Theme1.epic3.story3**  (2pts)
    
8.  **Theme1.epic3.story4**  (1pts)
    
9.  **Theme1.epic3.story5**  (2pts)
    
10.  **Theme1.epic4**  (3pts)
    
11.  **Theme2.epic1**  (3pts)
    
12.  **Theme2.epic2**  (3pts)
    
13.  **Theme2.epic3.story1**  (4pts)
    
14.  **Theme2.epic3.story2**  (4pts)
    
15.  **Theme2.epic4.story1**  (2pts)
    
16.  **Theme2.epic4.story2**  (2pts)
    
17.  **Theme2.epic5**  (3pts)

# Icebox 

***Epic 1 :*** Develop a recommendation bar to suggest alterante goals and alternate completion dates for success of the projects 
- **Story 1:** Integrate the model with this functionality 
- **Story 2:** Integrate the UI with this functionality 



# Repo Structure

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── add_songs.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```

