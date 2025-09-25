from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum, Q, F
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from .models import (
    PricingPlan, Customer, Subscription, Invoice, 
    PricingSettings, AuditLog
)
from .serializers import (
    PricingPlanSerializer, CustomerSerializer, SubscriptionSerializer,
    InvoiceSerializer, PricingSettingsSerializer, AuditLogSerializer,
    PricingDashboardSerializer, PlanComparisonSerializer,
    CustomerAnalyticsSerializer, DetailedPricingPlanSerializer,
    DetailedCustomerSerializer, DetailedSubscriptionSerializer
)


class PricingPlanViewSet(viewsets.ModelViewSet):
    """ViewSet for managing pricing plans"""
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedPricingPlanSerializer
        return PricingPlanSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active pricing plans"""
        plans = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured pricing plans"""
        plans = self.queryset.filter(is_featured=True, is_active=True)
        serializer = self.get_serializer(plans, many=True)
        return Response(serializer.data)


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for managing customers"""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedCustomerSerializer
        return CustomerSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active customers"""
        customers = self.queryset.filter(status='active')
        serializer = self.get_serializer(customers, many=True)
        return Response(serializer.data)


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing subscriptions"""
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailedSubscriptionSerializer
        return SubscriptionSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active subscriptions"""
        subscriptions = self.queryset.filter(status='active')
        serializer = self.get_serializer(subscriptions, many=True)
        return Response(serializer.data)


class InvoiceViewSet(viewsets.ModelViewSet):
    """ViewSet for managing invoices"""
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """Get all pending invoices"""
        invoices = self.queryset.filter(status__in=['draft', 'sent'])
        serializer = self.get_serializer(invoices, many=True)
        return Response(serializer.data)


class PricingSettingsViewSet(viewsets.ModelViewSet):
    """ViewSet for managing pricing settings"""
    queryset = PricingSettings.objects.all()
    serializer_class = PricingSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Ensure only one settings instance exists
        if not PricingSettings.objects.exists():
            PricingSettings.objects.create()
        return PricingSettings.objects.all()


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing audit logs"""
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]


class PricingDashboardViewSet(viewsets.ViewSet):
    """ViewSet for pricing dashboard data"""
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """Get dashboard data"""
        # Calculate basic metrics
        total_customers = Customer.objects.count()
        active_subscriptions = Subscription.objects.filter(status='active').count()
        
        # Calculate revenue
        total_revenue = Invoice.objects.filter(status='paid').aggregate(
            total=Sum('total_amount')
        )['total'] or Decimal('0.00')
        
        dashboard_data = {
            'total_customers': total_customers,
            'active_subscriptions': active_subscriptions,
            'total_revenue': total_revenue,
            'monthly_revenue': Decimal('0.00'),
            'pending_invoices': 0,
            'overdue_invoices': 0,
            'trial_subscriptions': 0,
            'popular_plan': 'None',
            'revenue_by_plan': {},
            'monthly_revenue_trend': [],
        }
        
        serializer = PricingDashboardSerializer(dashboard_data)
        return Response(serializer.data)
