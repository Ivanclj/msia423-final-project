# Midpoint Check

based on master branch, added the following files:

https://github.com/tiannfff/msia423-final-project/blob/midproject/src/upload_data.py

https://github.com/tiannfff/msia423-final-project/blob/midproject/src/import_data.py

https://github.com/tiannfff/msia423-final-project/blob/midproject/src/sql/models.py

Makefile: for convenient execution

Note: Please clone or download this repo before proceeding. upload_data.py needs to be run in AWS so please clone this repo to the AWS environment.

#### Setup Environment with `conda`

```bash
conda create -n pennylane python=3.7
conda activate pennylane
pip install -r requirements.txt

```

## import_data.py: 
download data from a GitHub repo to path_to_repo/data/Churn_Modelling.csv

command to run: 1) cd path_to_repo/src 2) in import_data.py, change save_path to "../data/Churn_Modelling.csv" 3) python import_data.py

OR using Makefile

command to run: 1) cd path_to_repo 2) keep save_path "data/Churn_Modelling.csv" 3) make get_data

## upload_data.py: 
upload data to target s3 bucket, be sure to configure the aws credential in advance

Parameters to be specified:
--input_path: local file path to data, e.g., ../data/Churn_Modelling.csv
--bucket_name: target bucket name
--output_path: s3 destination file path

command to run: 1) cd path_to_repo/src 2) python upload_data.py --input_file_path ../data/sample/Churn_Modelling.csv --bucket_name my-s3-bucket-name --output_file_path churn_data.csv

## models.py: 
create a local database or a db on RDS

Parameters to be specified:
--RDS: True to create RDS table, default is False (to create local db in sql/)

command to run: 1) cd path_to_repo/src/sql 2) python models.py --RDS True

Note: check if table is created successfully in logfile
