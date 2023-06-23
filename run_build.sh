#!/bin/bash

abort()
{
    echo "*** FAILED ***" >&2
    exit 1
}

if [ "$#" -eq 0 ]; then
    echo "No arguments provided. Usage: 
    1. '-local' to build local environment
    2. '-docker' to build and run docker container
    3. '-test' to run linter, formatter and tests"
elif [ $1 = "-local" ]; then
    trap 'abort' 0
    set -e
    echo "Running format, linter and tests"
    rm -rf .venv
    python3 -m venv .venv
    source .venv/bin/activate
    ./.venv/bin/pip install --upgrade pip
    ./.venv/bin/pip install -r ./requirements.txt

    black smarti tests
    pylint --fail-under=9.5 smarti tests
    pytest --cov-fail-under=5 --cov smarti -v tests
elif [ $1 = "-test" ]; then
    trap 'abort' 0
    set -e
    
    echo "Running format, linter and tests"
    source .venv/bin/activate
    black smarti tests
    pylint --fail-under=9.5 smarti tests
    pytest --cov-fail-under=5 --cov smarti -v tests
elif [ $1 = "-docker" ]; then
    echo "Building and running docker image"
    docker stop smarti-container
    docker rm smarti-container
    docker rmi smarti-image
    # build docker and run
    docker build --tag smarti-image --build-arg CACHEBUST=$(date +%s) .
    docker run --name smarti-container -p 8888:8888 -d smarti-image
else
  echo "Wrong argument is provided. Usage:
    1. '-local' to build local environment
    2. '-docker' to build and run docker container
    3. '-test' to run linter, formatter and tests"
fi

trap : 0
echo >&2 '*** DONE ***'

