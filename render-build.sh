cat <<EOF > render-build.sh
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# This runs the database initialization
python app.py
EOF
