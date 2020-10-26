APIDOC_OPTIONS = -d 1 --no-toc --separate --force --private
SOURCE_DIR = carinsurance

.PHONY: init

init:
	. init.sh

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.dev.txt

install-doc:
	pip install -r requirements.doc.txt

init-doc: install-doc # should not be used
	cd docs/; sphinx-quickstart

doc:
	rm -rf docs/source/generated
	sphinx-apidoc $(APIDOC_OPTIONS) -o docs/source/generated/ $(SOURCE_DIR) tests
	mkdir -p docs/source/_static
	cd docs; make html

dataset:
	python carinsurance/application/train/download_datasets.py

preprocessing:
	python carinsurance/application/train/preprocess_datasets.py

training:
	python carinsurance/application/train/train_model.py

local-api:
	gunicorn -b 0.0.0.0:8080 carinsurance.application.api.wsgi:app

api:
	gcloud app deploy app.yaml doc.yaml form.yaml

local-send:
	curl -H "Content-Type: application/json" -H "Accept-Charset: UTF-8" --request POST http://localhost:8080/api/ -d @${FILE}

send:
	curl -H "Content-Type: application/json" -H "Accept-Charset: UTF-8" --request POST ${URL} -d @${FILE}

local-form:
	gunicorn -b 0.0.0.0:8080 form:server
