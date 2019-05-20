import pandas as pd
import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from generate_features import choose_features
from train_model import split_data
from evaluate_model import evaluate_model

def test_choose_features():
    # load sample test data
    data = pd.read_csv("test/test_data.csv")

    features = ['CreditScore', 'Tenure', 'NumOfProducts', 'HasCrCard']

    # desired output dataframe
    output_df = data[['CreditScore', 'Tenure', 'NumOfProducts', 'HasCrCard', 'Exited']]
    
    # raise AssertionError if dataframes do not match
    assert output_df.equals(choose_features(df=data, features_to_use=features, target='Exited'))

def test_split_data():
    # load sample test data
    data = pd.read_csv("test/test_data.csv")
    X_df = data.drop('Exited',axis=1)
    y_df = data['Exited']
    X_train, X_test, y_train, y_test = train_test_split(X_df, y_df, test_size=0.3, random_state=123)

    # split data using the function
    X, y = split_data(X_df, y_df, train_size=0.7, test_size=0.3, random_state=123)

    # raise AssertionError if keys do not match
    assert X_train.equals(X['train'])
    assert y_test.equals(y['test'])

def test_evaluate_model():
    # test data input
    score_input = {'pred': [1,0,1,1,1,0,0,1,0,1],
                   'pred_prob': [0.998,0,0.99,0.914,0.993,0,0.006,0.999,0.00046,0.999]}
    label_input = {'class':[0,1,0,1,0,1,0,0,1,0]}

    score_df = pd.DataFrame(score_input)
    label_df = pd.DataFrame(label_input)

    # desired output dataframe
    output = confusion_matrix(label_df, score_df.iloc[:,0])
    output_df = pd.DataFrame(output,
        index=['Actual Negative','Actual Positive'],
        columns=['Predicted Negative', 'Predicted Positive'])
    
    # add kwargs for function
    pre_defined_kwargs = {'metrics':["confusion_matrix"]}
    # raise AssertionError if dataframes do not match
    assert output_df.equals(evaluate_model(label_df, score_df, **pre_defined_kwargs))

