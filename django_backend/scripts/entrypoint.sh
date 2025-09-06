#!/bin/bash
set -e

# Waiting db is ready
echo "Waiting for database..."
until pg_isready -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Database not ready, waiting..."
  sleep 2
done
echo "Database is ready ✅"

# MIGRATIONS
if [ "$SERVICE" = "web" ] || [ "$1" = "python" ]; then
    echo "Applying database migrations..."
    python manage.py migrate --noinput
    
    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    # CREATE SUPERUSER IF VARIABLES EXIST - DENTRO del primer if
    if [ ! -z "$DJANGO_SUPERUSER_USERNAME" ] && [ ! -z "$DJANGO_SUPERUSER_EMAIL" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser..."
        python manage.py createsuperuser \
            --username $DJANGO_SUPERUSER_USERNAME \
            --email $DJANGO_SUPERUSER_EMAIL \
            --noinput || echo "Superuser already exists or not created"
    fi
fi

# For specific commands
if [ "$1" = "python" ] && [ "$2" = "manage.py" ]; then
    echo "Starting server..."
    exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi

if [ "$1" = "celery" ]; then
    echo "Starting Celery $2..."
    exec "$@"
fi

exec "$@"