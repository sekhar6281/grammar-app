#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# This runs your script but we need it to stop after init_db
# We will use a python one-liner to just call the function
python -c "from app import init_db; init_db()"
