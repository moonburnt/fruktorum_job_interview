#!/bin/bash

echo "Waiting for postgres to startup"
sleep 10
echo "Running migrations"
python backend/manage.py makemigrations
python backend/manage.py migrate

echo "Setting up superuser"
export DJANGO_SUPERUSER_PASSWORD="adm1n_PASSWORD"
python backend/manage.py createsuperuser --username admin --email admin@mail.com --noinput

exec "$@"
