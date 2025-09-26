#!/bin/bash
set -e

echo "Starting Django application..."

# Check if database is accessible
echo "Testing database connection..."
python manage.py check --database default

# Apply all migrations in the correct order
echo "Applying all migrations..."
python manage.py migrate --noinput

# Start the application
echo "Starting gunicorn server..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 pricing_service.wsgi:application
