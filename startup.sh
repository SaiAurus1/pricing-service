#!/bin/bash
set -e

echo "Starting Django application..."

# Wait for database to be ready
echo "Waiting for database to be ready..."
python -c "
import time
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricing_service.settings_railway')
django.setup()
from django.db import connection
max_attempts = 30
for i in range(max_attempts):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
        print('Database is ready!')
        break
    except Exception as e:
        print(f'Database not ready, attempt {i+1}/{max_attempts}: {e}')
        if i == max_attempts - 1:
            raise
        time.sleep(2)
"

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --noinput

# Create superuser if it doesn't exist
echo "Creating superuser..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricing_service.settings_railway')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
"

# Test the application
echo "Testing application..."
python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricing_service.settings_railway')
django.setup()
from django.test import Client
client = Client()
response = client.get('/')
print(f'Root endpoint: {response.status_code}')
response = client.get('/health/')
print(f'Health endpoint: {response.status_code}')
"

# Start gunicorn
echo "Starting gunicorn server..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 --timeout 120 --access-logfile - --error-logfile - --log-level info pricing_service.wsgi:application
