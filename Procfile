web: python manage.py migrate && gunicorn --bind 0.0.0.0:$PORT --workers 3 pricing_service.wsgi:application
