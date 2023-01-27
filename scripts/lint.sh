#!/bin/bash

APP_PATH="django_drf_async"


echo "Running ruff checks on  ($APP_PATH)"
ruff $APP_PATH

echo "Running black checks on  ($APP_PATH)"
black $APP_PATH --check

echo "Running isort checks on ($APP_PATH)"
isort $APP_PATH --check-only
