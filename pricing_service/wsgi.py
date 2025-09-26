"""
WSGI config for pricing service.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricing_service.settings_railway')

application = get_wsgi_application()
