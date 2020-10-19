.PHONY: init

init:
	. init.sh

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.dev.txt

api:
	gunicorn -b 0.0.0.0:8080 carinsurance.application.api.wgsi:app
