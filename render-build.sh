cat <<EOF > render-build.sh
#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Install dependencies into the current environment
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 2. Force install gunicorn again just to be safe
python -m pip install gunicorn

# 3. Initialize your database
python app.py
EOF
