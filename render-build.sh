#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run your init_db logic if the DB doesn't exist
python app.py
