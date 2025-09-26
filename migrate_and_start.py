#!/usr/bin/env python3
"""
Migration and startup script for Railway deployment.
This script handles migrations in the correct order and starts the application.
"""
import os
import sys
import django
import time
from django.core.management import execute_from_command_line

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricing_service.settings_railway')
django.setup()

def wait_for_database():
    """Wait for database to be ready."""
    from django.db import connection
    max_attempts = 30
    
    for i in range(max_attempts):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            print('Database is ready!')
            return True
        except Exception as e:
            print(f'Database not ready, attempt {i+1}/{max_attempts}: {e}')
            if i == max_attempts - 1:
                raise
            time.sleep(2)
    return False

def apply_migrations():
    """Apply migrations in the correct order."""
    print("Applying migrations...")
    
    # First, apply Django built-in migrations
    print("Applying Django built-in migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', 'auth', '--noinput'])
        print("✓ Auth migrations applied")
    except Exception as e:
        print(f"Auth migration error: {e}")
        raise
    
    try:
        execute_from_command_line(['manage.py', 'migrate', 'admin', '--noinput'])
        print("✓ Admin migrations applied")
    except Exception as e:
        print(f"Admin migration error: {e}")
        raise
    
    try:
        execute_from_command_line(['manage.py', 'migrate', 'contenttypes', '--noinput'])
        print("✓ Contenttypes migrations applied")
    except Exception as e:
        print(f"Contenttypes migration error: {e}")
        raise
    
    try:
        execute_from_command_line(['manage.py', 'migrate', 'sessions', '--noinput'])
        print("✓ Sessions migrations applied")
    except Exception as e:
        print(f"Sessions migration error: {e}")
        raise
    
    # Then apply custom app migrations
    print("Applying custom app migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', 'pricing', '--noinput'])
        print("✓ Pricing migrations applied")
    except Exception as e:
        print(f"Pricing migration error: {e}")
        raise
    
    print("All migrations completed successfully!")

def create_superuser():
    """Create a superuser if it doesn't exist."""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            print('No superuser found, creating one...')
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            print('Superuser created: admin/admin123')
        else:
            print('Superuser already exists')
    except Exception as e:
        print(f'Error creating superuser: {e}')

def main():
    """Main function."""
    print("Starting Django application...")
    
    # Wait for database
    print("Waiting for database to be ready...")
    wait_for_database()
    
    # Apply migrations
    apply_migrations()
    
    # Create superuser
    create_superuser()
    
    # Start gunicorn
    print("Starting gunicorn server...")
    port = os.environ.get('PORT', '8000')
    os.execvp('gunicorn', [
        'gunicorn',
        '--bind', f'0.0.0.0:{port}',
        '--workers', '3',
        '--timeout', '120',
        'pricing_service.wsgi:application'
    ])

if __name__ == '__main__':
    main()
