#!/usr/bin/env bash

set -e

cd ${APP_DIR}

export PYTHONPATH=${PYTHONPATH}:${APP_DIR}

function start_server {
    pipenv run python app.py runserver
}

function start_server_dev {
    pipenv run python app.py migrate
    pipenv run python app.py runserver
}

function run_tests {
    pipenv run python app.py test
}

case "$1" in
    "run-server" ) start_server ;;
    "run-server-dev" ) start_server_dev ;;
    "test" ) run_tests ;;
    "bash" ) bash ;;
    "python" ) pipenv run python ;;
    *) echo "Command not recognized"; exit 1 ;;
esac
