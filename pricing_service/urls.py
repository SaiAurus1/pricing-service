"""
URL configuration for pricing service.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def root_view(request):
    """Simple root endpoint for health checks"""
    return JsonResponse({
        'service': 'pricing-service',
        'status': 'running',
        'version': '1.0.0'
    })

urlpatterns = [
    path('', root_view, name='root'),
    path('admin/', admin.site.urls),
    path('api/', include('pricing.urls')),
]
