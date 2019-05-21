"""
Created on 5/12/19

@author: Tian Fu

"""

import pandas as pd

def download_data(read_path,save_path):
    df = pd.read_csv(url,index_col=0)
    df.to_csv(save_path)


if __name__ == "__main__":
    # path to raw data on github
    url = 'https://raw.githubusercontent.com/tiannfff/msia423-final-project/master/data/sample/Churn_Modelling.csv'
    download_data(url,"./data/sample/Churn_Modelling.csv")

