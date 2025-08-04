#!/bin/bash

echo "Installing dependencies..."
python3 -m pip install -r requirements.txt || exit 1

echo "Collecting static files..."
python3 manage.py collectstatic --noinput || exit 1

echo "Build success!"
