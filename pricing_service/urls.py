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

def health_view(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'pricing-service'
    })

urlpatterns = [
    path('', root_view, name='root'),
    path('health/', health_view, name='health'),
    path('health', health_view, name='health_alt'),
    path('admin/', admin.site.urls),
    path('api/', include('pricing.urls')),
]
