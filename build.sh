#!/usr/bin/env bash
# exit on error

set -o errexit

pip install -r requirements.txt

pythoon manage.py collectstatic --noinput
python manage.py migrate
