.PHONY: init

init:
	. init.sh

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.dev.txt

dataset:
	python carinsurance/application/train/download_datasets.py

preprocessing:
	python carinsurance/application/train/preprocess_datasets.py

training:
	python carinsurance/application/train/train_model.py

api:
	gunicorn -b 0.0.0.0:8080 carinsurance.application.api.wgsi:app

deployment:
	gcloud app deploy

browse:
	gcloud app browse
