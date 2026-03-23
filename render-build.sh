cat <<EOF > render-build.sh
#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Initialize your grammar.db
python app.py
EOF
