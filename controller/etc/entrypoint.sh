#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:8080 config.wsgi