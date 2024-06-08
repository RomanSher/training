#!/bin/bash

until pg_isready -d "$DB_NAME" -h "$DB_HOST" -p 5432 -U "$DB_USER"; do
    echo "$(date) - waiting for postgres on DB_NAME: $DB_NAME, DB_HOST: $DB_HOST, DB_USER: $DB_USER"
    sleep 5
done

yes yes | python manage.py runserver 0.0.0.0:8000