#!/bin/bash

pipenv run pip freeze > requirements.txt
docker build -t fbexp:latest .
