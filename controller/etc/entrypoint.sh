#!/bin/bash

#python -m ptvsd --host 0.0.0.0 --port 5678 --wait --multiprocess manage.py runserver 0.0.0.0:8000
python manage.py runserver 0.0.0.0:8000

# gunicorn --bind 0.0.0.0:8000 config.wsgi
