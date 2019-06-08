MODEL_NAME=GradientBoosting.pkl
CONFIG=config.yml
BUCKET=bin

.PHONY: load_data clean train_model evaluate_model venv clean_dir 

kickstart/${BUCKET}/activate: requirements.txt
	test -d kickstart ||    virtualenv kickstart
	. kickstart/${BUCKET}/activate; pip install -r requirements.txt
	touch kickstart/${BUCKET}/activate

venv: kickstart/${BUCKET}/activate

clean_dir:
	test -d data |  rm -rf data
	test -d clean | rm -rf clean
	test -d models |    rm -rf models
	test -d eval |    rm -rf eval
	mkdir data
	mkdir clean
	mkdir models
	mkdir eval

data/raw.csv: venv clean_dir
	. kickstart/${BUCKET}/activate; python run.py ingest_data

load_data: data/raw.csv venv
	. kickstart/${BUCKET}/activate

clean/cleaned_data.csv: data/raw.csv venv
	. kickstart/${BUCKET}/activate; python run.py Returns_cleaned_data

clean_data: clean/cleaned_data.csv venv
	. kickstart/${BUCKET}/activate


models/${MODEL_NAME}: clean/cleaned_data.csv venv
	. kickstart/${BUCKET}/activate; python run.py Model_fitting

train_model: models/${MODEL_NAME} venv
	. kickstart/${BUCKET}/activate

eval/evaluate.txt: models/${MODEL_NAME} venv
	. kickstart/${BUCKET}/activate; python run.py eval

evaluate_model: eval/evaluate.txt venv
	. kickstart/${BUCKET}/activate

all: evaluate_model venv
	. kickstart/${BUCKET}/activate