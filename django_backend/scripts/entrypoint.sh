#!/bin/bash
set -e

echo "Creating migrations structure..."
for app in tasks users api; do
    if [ -d "apps/$app" ]; then
        mkdir -p "apps/$app/migrations"
        touch "apps/$app/migrations/__init__.py"
        echo "Created migrations structure for $app"
    fi
done

# Waiting db is ready
echo "Waiting for database..."
until pg_isready -h db -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Database not ready, waiting..."
  sleep 2
done
echo "Database is ready ✅"

# MIGRATIONS
if [ "$SERVICE" = "web" ] || [ "$1" = "python" ]; then
    echo "Creating database migrations..."
    python manage.py makemigrations --noinput
    
    echo "Applying database migrations..."
    python manage.py migrate --noinput
    
    echo "Collecting static files..."
    python manage.py collectstatic --noinput

    # CREATE SUPERUSER
    if [ ! -z "$DJANGO_SUPERUSER_USERNAME" ] && [ ! -z "$DJANGO_SUPERUSER_EMAIL" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
        echo "Creating superuser..."
        python manage.py createsuperuser \
            --username "$DJANGO_SUPERUSER_USERNAME" \
            --email "$DJANGO_SUPERUSER_EMAIL" \
            --noinput || echo "Superuser already exists or not created"
    fi
    
    echo "Starting server..."
    exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi

# For celery services
if [ "$1" = "celery" ]; then
    echo "Starting Celery $2..."
    exec "$@"
fi

exec "$@"