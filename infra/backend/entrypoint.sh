#!/bin/sh

echo "Waiting for PostgreSQL..."

while ! nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 1
done

echo "PostgreSQL started"

python manage.py migrate

python manage.py loaddata db || true

python manage.py collectstatic --noinput

cp -r /app/staticfiles/. /backend_static/static/

gunicorn bio_clinic.wsgi:application --bind 0.0.0.0:8000