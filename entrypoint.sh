#!/bin/sh

# Wait for DB to be ready (optional for Postgres)
# echo "Waiting for database..."
# sleep 5

# Run migrations
python manage.py migrate

# Collect static files (optional)
# python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn oj.wsgi:application --bind 0.0.0.0:8000
