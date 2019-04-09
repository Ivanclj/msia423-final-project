# Example project repository

<!-- toc -->

- [Project Charter](#project-charter)
- [Project Backlog](#project-backlog)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv-and-pip)
    + [With `conda`](#with-conda)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter 

**Vision**: Evaluate opportunities for marketing and product improvements, and ultimately enhance customer retention and engagement to develop the bank services and enlarge customer base. 

**Mission**: By analyzing customers’ demographic and account information to evaluate whether or not they will churn, keep track of this bank’s customer retention rates to facilitate the study of characteristics of two groups of customers to inform targeting, improve products, and enhance customer engagement.

**Success criteria**: The machine learning success criteria for this classification model is a prediction accuracy over 80%, and precision and recall over 70%; will also look at AUC. The business outcome metric is the measure of customer retention (see if the retention rate is increasing and matches this bank’s goal).


## Project Backlog  

**Themes**: 
Explore of various patterns in customer base across churn and no churn (loyal customers) groups to provide insights into plans that stimulate customer engagement.

Development of methods for identifying whether or not a customer of this bank will churn or not based his/her selected information.

Display of trends in customer retentions as the app is being used for a continuous time, in order to discover any pattern indicative of the need to improve product or marketing.

**Epic 1**: Explore existing customers to study their behaviors related to churn.
 - Backlog 1 (for next two weeks): Understand overall distribution of attributes across all customers. 
	 - Time Estimation: 2 points
 - Backlog 2 (for next two weeks): Display distribution of different attributes across churn and no churn groups to see if there is a differentiated pattern. The bank will then be able to look for patterns in other customers and come up with plans to retain old customers or attract new customers elsewhere.
	 - Time Estimation: 2 points 
 - Backlog 3: Other exploratory analysis based on demographic groups such as country, gender, age to explore if a specific group is loyal customer to this bank and develop strategy to drive further customer engagement.
	 - Time Estimation: 2 points

**Epic 2**: Predict whether a customer will churn or not based on geographic and account information obtained from the bank in 2019.
 - Backlog 1: Use a crude model to select most important features from all attributes that help predict the likelihood of churn.
	 - Time Estimation: 1 point
 - Backlog 2: Model this classification problem using selected features and optimized hyperparameters (model complexity and performance-wise) to achieve the success criteria.
	 - Time Estimation: 4 points
 - Backlog 3: As new customer information being entered in the app, whether this customer will likely to churn or not churn will be predicted. Possibly compare his/her feature with others in the same group to study the possible reasons for exit.
	 - Time Estimation: 4 points
 - Icebox: Update the customer information as the same not-churned customer is recorded into the app. As updated customer information will impact prediction result, a new model needs to be implemented based on updated information each month/quarter/year.
	 - Time Estimation: 8 points

**Epic 3**: Keep track of customer retentions within the company as more customers are added. The bank might have a certain goal as to what percentage of customers it wants to retain each year. If that is not met, then the bank has to evaluate its product, customer service, or marketing campaigns to increase retention.
 - Backlog: Document current retention rate and recalculate customer retention each trial/month/quarter/year as new customers are added through the app on a continuous basis.
	 - Time Estimation: 1 point
 - Icebox: Visualize customer retention over time and investigate characteristics of exited customers.
	 - Time Estimation: 8 points since a large time interval required to see trends.


## Repo structure 

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
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv pennylane

source pennylane/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n pennylane python=3.7
conda activate pennylane
pip install -r requirements.txt

```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3002  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'  # URI for database that contains tracks

```


### 3. Initialize the database 

To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

To add additional songs:

`python run.py ingest --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`


### 4. Run the application 
 
 ```bash
 python app.py 
 ```

### 5. Interact with the application 

Go to [http://127.0.0.1:3000/]( http://127.0.0.1:3000/) to interact with the current version of hte app. 

## Testing 

Run `pytest` from the command line in the main project repository. 


Tests exist in `test/test_helpers.py`
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTEyNTQ5NzYwNV19
-->