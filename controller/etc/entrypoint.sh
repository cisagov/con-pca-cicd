#!/bin/bash

echo "Collecting static files"
python manage.py collectstatic --no-input

echo "Initialize application"
python scripts/init.py &

python manage.py runserver 0.0.0.0:8000
