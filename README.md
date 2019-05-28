## Developer: Tian Fu
## QA: Yueying(Sharon) Zhang
# Outline

<!-- toc -->

- [Project Charter](#project-charter)
- [Project Planning](#project-planning)
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

**Mission**: Compare demographic and account information across customers who have churned and who have not churned and use these information to predict whether or not a new customer will churn. Keeping track of this bank’s customer retention rates facilitates the study of characteristics of two groups of customers to inform targeting, improve products, and enhance customer engagement.

**Success criteria**: The baseline machine learning success criteria for this classification model is an AUC score of over 70%; will also look at F1-score. The business outcome metric is the measure of customer retention (see if the retention rate is increasing and matches this bank’s goal).

Data Source: https://www.kaggle.com/shrutimechlearn/churn-modelling

## Project Planning  

**Themes**: 
Explore of various patterns in customer base across churn and no churn (loyal customers) groups to provide insights into plans that stimulate customer engagement.

Development of methods for identifying whether or not a customer of this bank will churn or not based his/her selected information.

Display of trends in customer retentions as the app is being used for a continuous time, in order to discover any pattern indicative of the need to improve product or marketing.

**Epic 1**: Explore existing customers to study their behaviors related to churn.
 - Story 1: Understand overall distribution of attributes across all customers. 
 - Story 2: Display distribution of different attributes across churn and no churn groups to see if there is a differentiated pattern. For example, churned customers might have less accounts in this bank. The bank will then be able to look for these patterns in other customers not in the sample and come up with plans to retain old customers or attract new customers elsewhere.
 - Story 3: Other exploratory analysis based on demographic groups such as country, gender, age to explore if a specific group is loyal customer to this bank and develop strategy to drive further customer engagement. For example, maybe German customers are less likely to churn. This might be due to the bank's unique marketing strategy in Germany. They could think about applying similar strategies in other countries to improve customer retention.

**Epic 2**: Predict whether a customer with obtained demographic and account information in 2019 will churn or not.
 - Story 1: Use a crude model to select most important features from all attributes that help predict the likelihood of churn.
 - Story 2: Model this classification problem using selected features through different model approaches.
 - Story 3: Choose optimized hyperparameters (model complexity and performance-wise) to achieve the success criteria.
 - Story 4: As new customer information being entered in the app, whether this customer will likely to churn or not churn will be predicted. Possibly compare his/her feature with others in the same group to study the possible reasons for exit.

**Epic 3**: Deploy the model onto AWS and develop the churn prediction App. Keep track of customer retentions within the company as more customers are added.
 - Story 1: Document current retention rate and recalculate customer retention each trial/quarter/year as new customers are added through the app on a continuous basis. The bank might have a certain goal as to what percentage of customers it wants to retain each year. If that is not met, then the bank has to evaluate its product, customer service, or marketing campaigns to increase retention.

### Backlog
1. Theme.epic1.story1: General Exploration (2 points) 
2. Theme.epic1.story2: Understanding Two Groups (2 points) 
3. Theme.epic1.story3: Demographic Group Exploration (2 points)
4. Theme.epic2.story1: Feature Selection (1 point)
5. Theme.epic2.story2: Model Building (4 points)
6. Theme.epic2.story3: Hyperparameter Tuning (4 points)
7. Theme.epic2.story4: Prediction (4 points)
8. Theme.epic3.story1: Deployment (8 points)

### Icebox
1. Transit from Local to AWS and develop the App.
	 - Time Estimation: 8 points
	 - Will break this icebox down as become more familiar with AWS and App development.
2. Update the customer information as the same not-churned customer is recorded into the app. As updated customer information will impact prediction result, a new model needs to be implemented based on updated information each month/quarter/year.
	 - Time Estimation: 8 points
3.  Look at the distribution of churn probability among customers. Instead of using a threshold of 0.5, adjust threshold based on the bank's target, which will result in different retention rates and different proportion of active customers.
	 - Time Estimation: 8 points
4. Visualize customer retention over time and investigate characteristics of exited customers.
	 - Time Estimation: 8 points since a large time interval required to see trends.

## Repo structure 

```
├── README.md                         <- You are here
│
├── app 
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for feature generation, model training, scoring, etc.
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│   ├── database/                     <- Database with initial customers used for app, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and model evaluations.
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
│   ├── helpers/                      <- Helper scripts used in main src files.
│   ├── sql/                          <- SQL source code.
│   ├── import_data.py                <- Script for downloading raw data from github. 
│   ├── upload_data.py                <- Script for uploading data files to S3 bucket. 
│   ├── load_data.py                  <- Script for loading data files saved to desired location. 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for training and scoring.
│   ├── train_model.py                <- Script for training a machine learning model.
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── evaluate_model.py             <- Script for evaluating model performance.
│   ├── test.py                       <- Script for running unit tests on functions in src/.
│   ├── README.md                     <- Documentation for midproject check instructions.
│
├── test                              <- Files necessary for running model tests (see documentation below) 
│
├── static/                           <- CSS, JS files that remain static
├── templates/                        <- HTML (or other code) that is templated and changes based on a set of inputs
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
(optional): to solve Command 'pip' not found: conda install pip then pip install -r requirements.txt

```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3002  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/database/churn_prediction.db'  # URI for database that contains tracks

```


### 3. Initialize the database 

To create the database in the location configured in `config.py` with five initial customers, run: 

`1) cd path_to_repo/src`

`2) python models.py --RDS False`


### 4. Run the application 
 
 ```bash
 python app.py 
 ```

### 5. Interact with the application 

Go to [http://127.0.0.1:3002/]( http://127.0.0.1:3002/) to interact with the current version of the app. 

## Testing 

Run `make test` from the command line in the main project repository. 


Tests exist in `src/test.py`
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTQyOTcxNjUwNV19
-->
