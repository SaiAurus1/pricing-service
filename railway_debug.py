#!/usr/bin/env python3
"""
Debug script for Railway deployment - check environment variables and database connection.
"""
import os
import sys
import django
from django.conf import settings

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricing_service.settings_railway')
django.setup()

def check_environment():
    """Check all required environment variables."""
    print("=== Environment Variables Check ===")
    
    required_vars = [
        'DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT',
        'DJANGO_SECRET_KEY'
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if 'PASSWORD' in var or 'SECRET' in var:
                print(f"✓ {var}: {'*' * len(value)}")
            else:
                print(f"✓ {var}: {value}")
        else:
            print(f"✗ {var}: NOT SET")

def check_database():
    """Test database connection."""
    print("\n=== Database Connection Test ===")
    
    try:
        from django.db import connection
        connection.ensure_connection()
        print("✓ Database connection successful")
        
        # Test a simple query
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print(f"✓ Database query test: {result}")
            
    except Exception as e:
        print(f"✗ Database connection failed: {e}")

def check_django_settings():
    """Check Django settings."""
    print("\n=== Django Settings Check ===")
    
    print(f"✓ SECRET_KEY: {'SET' if settings.SECRET_KEY else 'NOT SET'}")
    print(f"✓ DEBUG: {settings.DEBUG}")
    print(f"✓ Database Engine: {settings.DATABASES['default']['ENGINE']}")
    print(f"✓ Database Name: {settings.DATABASES['default']['NAME']}")
    print(f"✓ Database Host: {settings.DATABASES['default']['HOST']}")

if __name__ == "__main__":
    print("Railway Deployment Debug Script")
    print("=" * 40)
    
    check_environment()
    check_django_settings()
    check_database()
    
    print("\n" + "=" * 40)
    print("Debug complete!")
