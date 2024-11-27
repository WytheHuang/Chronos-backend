#!/bin/sh

python manage.py migrate
python run_asgi.py

exec "$@"
