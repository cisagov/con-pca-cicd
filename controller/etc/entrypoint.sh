#!/bin/bash
# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

python manage.py runserver 0.0.0.0:8000

# gunicorn --bind 0.0.0.0:8000 config.wsgi