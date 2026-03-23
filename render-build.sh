#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Force use of the environment's python to install everything
python -m pip install --upgrade pip
python -m pip install Flask==3.1.3 gunicorn==25.1.0

# 2. Initialize your database
python app.py
