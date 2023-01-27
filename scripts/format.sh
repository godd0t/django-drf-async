#!/bin/bash -e

APP_PATH="django_drf_async"

set -x

ruff $APP_PATH --fix
black $APP_PATH
isort $APP_PATH
