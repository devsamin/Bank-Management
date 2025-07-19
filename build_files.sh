#!/bin/bash

# make migrations and migrate the database
python3 manage.py makemigrations --noinput
python3 manage.py migrate --noinput

# collect static files
python3 manage.py collectstatic --noinput --clear
