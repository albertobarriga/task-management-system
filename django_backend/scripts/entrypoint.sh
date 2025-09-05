#!/bin/bash
set -e

# Waiting db is ready
echo "Waiting for database..."
until pg_isready -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Database not ready, waiting..."
  sleep 2
done
echo "Database is ready ✅"


if [ "$1" = "python" ] && [ "$2" = "manage.py" ]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput
    
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    
    echo "Starting server..."
    exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi

# For Celery services
if [ "$1" = "celery" ]; then
    echo "Starting Celery $2..."
    exec "$@"
fi

exec "$@"