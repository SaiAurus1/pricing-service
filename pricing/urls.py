from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PricingPlanViewSet, CustomerViewSet, SubscriptionViewSet,
    InvoiceViewSet, PricingSettingsViewSet, AuditLogViewSet,
    PricingDashboardViewSet, health_check
)

router = DefaultRouter()
router.register(r'plans', PricingPlanViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'settings', PricingSettingsViewSet)
router.register(r'audit-logs', AuditLogViewSet)
router.register(r'dashboard', PricingDashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
    path('health/', health_check, name='health_check'),
    path('health', health_check, name='health_check_alt'),  # Alternative endpoint
]
