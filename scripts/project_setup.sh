#!/bin/bash

PROJECT_NAME=${1}

touch ../$PROJECT_NAME/.gitignore
touch ../$PROJECT_NAME/requirements.txt
touch ../$PROJECT_NAME/README.md
#touch $PROJECT_NAME/LICENSE

mkdir -p ../$PROJECT_NAME/tests/unit
mkdir -p ../$PROJECT_NAME/tests/integration
mkdir -p ../$PROJECT_NAME/tests/system

mkdir -p ../$PROJECT_NAME/flask/templates

mkdir -p ../$PROJECT_NAME/sqlite

