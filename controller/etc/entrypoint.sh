#!/bin/bash

echo "Collecting static files"
python manage.py collectstatic --no-input

echo "Initialize application"
python scripts/init.py &

if [[ $DEBUG -eq 1 ]]
then
    echo "Run server"
    python manage.py runserver 0.0.0.0:8000
else
    echo "Serve using WSGI"
    gunicorn --bind 0.0.0.0:8000 config.wsgi #--keyfile /certs/server.key --certfile /certs/server.crt
fi
