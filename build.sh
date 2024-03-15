#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
pip install -r deploy-requirements.txt
python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata testdb.json
