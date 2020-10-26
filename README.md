# Car Insurance Demonstration

## Introduction

A company has to call customers in order to make them subscribe to their services. However, they want to help organizing the business by telling them which customers might follow up with a subscription or not. Indeed, they can organize better their resources for their work.

This project is a template for addressing this simple business problem with a simple form calling a REST API using a simple ML model to predict the subscription.

This project is also documented and available online (the [form](https://form-dot-blog-msok-ml-290723.ew.r.appspot.com) and the [documentation](https://doc-dot-blog-msok-ml-290723.ew.r.appspot.com).

The API route is located at https://blog-msok-ml-290723.ew.r.appspot.com/api/.

## Authors

- Michaël SOK - <mdb.sok@gmail.com>

## Project

The different commands were specified for a UNIX environment and might not be usable on Windows.

### GCP

The following commands assume that you set up correctly your gcp project (assuming that you have one, if not only the local commands would be used). For this, use the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install), initialize it with the command:

```bash
gcloud init
```

and follow the indications.

### Virtual Environment

#### Initialization

You can create a virtual environment with the Makefile command:
```bash
make init
```

or directly calling the `init.sh` file with:

```bash
. init.sh
```

If everything worked, you have received this messages:

```bash
=============================================
Virtual environment successfully created
It is located at:
/Users/michaelsok/projects/car-insurance/.venv
In order to activate this virtual environment
$ source activate.sh
=============================================
```

#### Activation

As specified in the previous section message, the virtual environment can be activated through the following command:

**If you want to work on local, replace in the `activate.sh` file the `export FORM_GCP_PROJECT="$(gcloud config get-value project)"` with `export FORM_GCP_PROJECT`**

```bash
source activate.sh
```

You now must have activated the virtual environment and seeing this message:

```bash
==========================================
Virtual environment successfully activated
You are now using this python:
/Users/michaelsok/projects/car-insurance/.venv/bin/python
==========================================
```

Also, the terminal command line must be preceded by your virtual environment name `.venv`, for instance:

```bash
(.venv) MacBook-Air-de-Michael:car-insurance michaelsok$
```

NB: the name might be a path if you're using `conda`

#### Installation

Now you should install the requirements for the project with the following make command:

```bash
make install
```

which is basically an alias for the famous `pip install -r requirements.txt`

### Training

#### Downloading the dataset

Before training the model you might need to download the data. For this, you first have to register on Kaggle and download a Kaggle json key which must be placed in `~/.kaggle/kaggle.json`.

Once done, you may run the followin make command:

```bash
make dataset
```

#### Preprocessing the dataset

You can now create a preprocessing pipeline with the following command:

```bash
make preprocessing
```

#### Training the model

Since this is an API template, not a demonstration of ML prowess, The model was nor hyper-tuned neither challenged. Thus it's a simple RandomForestClassifier, without any calibration or cross-validation. For training, you just have to launch the following command:

```bash
make training
```

You may find a classification report in the results directory using a validation set.

### Creating API examples

For this you just have to run

```bash
make examples
```

which create both batch and online examples

### Creating a local API

#### Creation

You can create a local REST API using the following command:

```bash
make local-api
```

the application use Flask and is served through gunicorn.

#### Testing

To test the API you have to change terminal since your API is running. 
You just have to run for an online prediction:

```bash
make local-send FILE=data/examples/online/online_4001.json
```

and 

```bash
make local-send FILE=data/examples/batch/batch.json
```

for a batch prediction.

### Creating a webapp

To create a webapp (the form), you only have to run:

```bash
make local-form
```

### Creating a documentation

```bash
make install-doc
make doc
```

### Deploying to Google App Engine

To deploy :

```bash
make api
```


### Code structure

The code contains two separate projects, the [api](/carinsurance) and the [form](/form).

#### API

The API code contains six directories:
- application
    - api
    - examples
    - train
- config
    - config.json
- domain
    - modelling
    - preprocessing
- helpers
    - preprocessing
- infrastructure
    - preprocessing
    - dataset.py
- interface
    - application.py
    - exceptions.py

##### application

In this directory are present the main files to launch for the different routines in the directories:
- train for downloading the dataset (download_datasets.py) as well as training both pipeline (preprocess_datasets.py) and model (train_model.py)
- examples for creating test examples to send to the API (create_test_examples.py)
- api for running the app (wsgi.py)

NB: for launching [download_datasets.py](/carinsurance/application/train/download_datasets.py) you must register to Kaggle and import the Kaggle key and place it at `~/.kaggle/kaggle.json`

##### config

It contains the configurable. You might want to place the kaggle key in this directory and change `keyname` in `config.json` with the corresponding filename.

##### domain

You'll find here any functions or classes with a business knowledge needed such as some specific preprocessing steps or the modelling (in the corresponding directories).

##### helpers

This directory contains some global functions or classes used throughout the project.

##### infrastructure

You'll find here any functions or classes with no business knowledge needed such as downloading dataset or basic operations on data.

##### interface

Here are specified any functions for creating the api objects (flask).
