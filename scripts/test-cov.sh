#!/bin/bash
APP_PATH="./"

export PYTHONPATH=$APP_PATH
set -e
set -x
pytest --cov=$APP_PATH --cov-report=xml
