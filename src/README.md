# Midpoint Check

based on master branch, added the following files:

https://github.com/tiannfff/msia423-final-project/blob/midproject/src/upload_data.py

https://github.com/tiannfff/msia423-final-project/blob/midproject/src/import_data.py

https://github.com/tiannfff/msia423-final-project/blob/midproject/src/sql/models.py

Makefile: for convenient execution

Note: Please clone or download this repo before proceeding. upload_data.py needs to be run in AWS so please clone this repo to the AWS environment, and cd <path_to_repo>

#### Setup Environment with `conda`

```bash
conda create -n pennylane python=3.7
conda activate pennylane
pip install -r requirements.txt

```

## import_data_github.py: 
download data from a GitHub repo to path_to_repo/data/Churn_Modelling.csv

command to run: 1) cd path_to_repo/src 2) in import_data_github.py, change save_path to "../data/Churn_Modelling.csv" 3) python import_data_github.py

OR using Makefile

command to run: 1) cd path_to_repo 2) keep save_path "data/Churn_Modelling.csv" 3) make get_data_github

## import_data_s3.py: 
download data from a public s3 bucket to path_to_repo/data/Churn_Modelling.csv

Parameters to be specified:

--sourceurl: link to source data in a public s3 bucket

--filename: target source file name

--savename: path where to save the file locally

command to run: 1) cd path_to_repo/src 2) python import_data_s3.py --sourceurl https://nw-tianfu-project-data.s3.us-east-2.amazonaws.com/Churn_Modelling.csv --filename Churn_Modelling.csv --savename ../data/Churn_Modelling.csv

OR using Makefile

command to run: 1) cd path_to_repo 2) make get_data_s3

## upload_data.py: 
upload data to target s3 bucket, be sure to configure the aws credential in advance

Parameters to be specified:

--input_path: local file path to data, e.g., ../data/Churn_Modelling.csv

--bucket_name: target bucket name

--output_path: s3 destination file path

--access_key_id: private s3 bucket access key id (default is None for public buckets)

--secret_access_key: private s3 bucket secret access key (default is None for public buckets)

command to run: 1) cd path_to_repo/src 2) python upload_data.py --input_file_path ../data/sample/Churn_Modelling.csv --bucket_name my-s3-bucket-name --output_file_path churn_data.csv --access_key_id <my_s3_access_key_id> --secret_access_key <my_s3_secret_access_key>

Note: no need to input last two arguments if your s3 bucket is public.

## models.py: 
create a local database or a db on RDS

Parameters to be specified:

--RDS: True to create RDS table, default is False (to create local db in data/database/); no need to specify it if running locally
--local_URI: default at sqlite:///../data/database/churn_prediction.db; no need to specify it

command to run: 1) cd path_to_repo/src 2) python models.py -> this will create a db locally

OR 1) cd path_to_repo/src 2) python models.py --RDS -> this will create a db locally

Note: check if table is created successfully in logfile
