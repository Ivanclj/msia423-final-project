import pandas as pd
import numpy as np
import pickle
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

from src.generate_features import choose_features, get_target, generate_features
from src.train_model import split_data
from src.evaluate_model import evaluate_model
from src.score_model import score_model

def test_choose_features():
    """Test the functionality of choose_features."""
    # load sample test data
    data = pd.read_csv("test/test_data.csv")

    features = ['CreditScore', 'Tenure', 'NumOfProducts', 'HasCrCard']

    # desired output dataframe
    output_df = data[['CreditScore', 'Tenure', 'NumOfProducts', 'HasCrCard', 'Exited']]
    
    # raise AssertionError if dataframes do not match
    assert output_df.equals(choose_features(df=data, features_to_use=features, target='Exited'))


def test_get_target():
    """Test the functionality of get_target."""
    # load sample test data
    data = pd.read_csv("test/test_data.csv")

    # desired output values
    output_values = data['Exited'].values
    
    # raise AssertionError if output values do not match element-wise
    assert (output_values==(get_target(df=data, target='Exited'))).all()


def test_generate_features():
    """Test the functionality of generate_features."""
    # load sample test data
    data = pd.read_csv("test/test_raw_data.csv")
    kwargs = {'choose_features':{'features_to_use': ['CreditScore','Tenure','NumOfProducts','Gender','Geography'],
                                 'target': 'Exited'},
            'to_dummy':['Gender','Geography']}
    # output dataframe
    output = data[['CreditScore','Tenure','NumOfProducts','Gender','Geography','Exited']]
    # convert two variables to dummies
    gender_dummy = pd.get_dummies(output['Gender'], drop_first=True)
    geo_dummy = pd.get_dummies(output['Geography'], drop_first=True)

    output.drop(['Gender','Geography'],axis=1,inplace=True)
    # new dataframe after encode categorical variables as dummies
    output = pd.concat([output,gender_dummy,geo_dummy], axis=1)

    assert output.equals(generate_features(df=data, save_features=None, **kwargs))


def test_split_data():
    """Test the functionality of split_data."""
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


def test_score_model():
    """Test the functionality of score_model."""
    path_to_tmo = 'test/test-model.pkl'
    # load sample test data
    data = pd.read_csv("test/test_data.csv")
    kwargs = {'none':'none'}
    X_data = data[['Age', 'Tenure', 'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'Germany', 'Male']]

    with open(path_to_tmo, "rb") as f:
        model = pickle.load(f)
    # get probability of churn
    y_prob = model.predict_proba(X_data)[:,1]
    output = pd.DataFrame(y_prob)
    output.columns = ['pred_prob']

    # assign class label based on threshold
    def predicted_label(row):
        """helper function for assign predicted labels."""
        if row['pred_prob'] > 0.6:
            return 1
        else:
            return 0
    output['pred'] = output.apply(lambda row: predicted_label(row), axis=1)
    
    assert output.equals(score_model(df=X_data, path_to_tmo=path_to_tmo, threshold=0.6, **kwargs))

def test_evaluate_model():
    """Test the functionality of evaluate_model."""
    # test data input
    score_input = {'pred_prob': [0.998,0,0.99,0.914,0.993,0,0.006,0.999,0.00046,0.999],
                   'pred': [1,0,1,1,1,0,0,1,0,1]}
    label_input = {'class':[0,1,0,1,0,1,0,0,1,0]}

    score_df = pd.DataFrame(score_input)
    label_df = pd.DataFrame(label_input)

    # desired output dataframe
    output = confusion_matrix(label_df, score_df.iloc[:,1])
    output_df = pd.DataFrame(output,
        index=['Actual Negative','Actual Positive'],
        columns=['Predicted Negative', 'Predicted Positive'])
    
    # add kwargs for function
    pre_defined_kwargs = {'metrics':["confusion_matrix"]}
    # raise AssertionError if dataframes do not match
    assert output_df.equals(evaluate_model(label_df, score_df, **pre_defined_kwargs))

