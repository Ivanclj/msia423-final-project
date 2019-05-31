.PHONY: features trained-model scores evaluation test clean-pyc clean-env 

# Create a virtual environment named pennylane-env
pennylane-env/bin/activate: requirements.txt
	test -d pennylane-env || virtualenv pennylane-env
	. pennylane-env/bin/activate; pip install -r requirements.txt
	touch pennylane-env/bin/activate

venv: pennylane-env/bin/activate

# Below are for reproducing feature generation, modeling, scoring, evaluation and post-process
data/churn_processed.csv: src/generate_features.py
	python run.py generate_features --config=config/model_config.yml --output=data/churn_processed.csv

features: data/churn_processed.csv

models/churn-prediction.pkl: data/churn_processed.csv src/train_model.py
	python run.py train_model --config=config/model_config.yml --input=data/churn_processed.csv --output=models/churn-prediction.pkl

trained-model: models/churn-prediction.pkl

models/churn_test_scores.csv: src/score_model.py
	python run.py score_model --config=config/model_config.yml --output=models/churn_test_scores.csv

scores: models/churn_test_scores.csv

models/model_evaluation.csv: src/evaluate_model.py
	python run.py evaluate_model --config=config/model_config.yml --output=models/model_evaluation.csv

evaluation: models/model_evaluation.csv


# Pull raw data from github
get_data:
	python src/import_data_github.py

# Run all tests
test:
	pytest test/test.py

# Clean up things
clean-tests:
	rm -rf .pytest_cache
	rm -r test/model/test/
	mkdir test/model/test
	touch test/model/test/.gitkeep

clean-env:
	rm -r pennylane-env

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	rm -rf .pytest_cache

clean: clean-env clean-pyc

all: features trained-model scores evaluation