#!/usr/bin/env python
"""
Setup script for pricing service.
Run this script to initialize the pricing service.
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricing_service.settings')

# Setup Django
django.setup()


def setup_pricing_service():
    """Setup the pricing service"""
    print("Setting up Pricing Service...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Please copy env.example to .env and configure your database settings.")
        return False
    
    # Run migrations
    print("Running migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations completed successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    # Create superuser if needed
    print("Creating superuser...")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            print("✅ Superuser created (username: admin, password: admin123)")
        else:
            print("✅ Superuser already exists")
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False
    
    print("\n🎉 Pricing Service setup completed!")
    print("\nNext steps:")
    print("1. Update your .env file with Railway database credentials")
    print("2. Deploy to Railway or run locally with: python manage.py runserver")
    print("3. Access admin at: http://localhost:8000/admin/")
    print("4. API endpoints available at: http://localhost:8000/api/")
    
    return True


if __name__ == '__main__':
    setup_pricing_service()
