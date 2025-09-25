from rest_framework import serializers
from .models import (
    PricingPlan, Customer, Subscription, Invoice, 
    PricingSettings, AuditLog
)
from decimal import Decimal


class PricingPlanSerializer(serializers.ModelSerializer):
    """Serializer for PricingPlan model"""
    monthly_price = serializers.ReadOnlyField()
    
    class Meta:
        model = PricingPlan
        fields = [
            'id', 'name', 'description', 'plan_type', 'billing_cycle',
            'base_price', 'setup_fee', 'max_loan_applications', 'max_users',
            'max_storage_gb', 'api_access', 'advanced_analytics',
            'priority_support', 'white_label', 'custom_integrations',
            'is_active', 'is_featured', 'created_at', 'updated_at',
            'monthly_price'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""
    
    class Meta:
        model = Customer
        fields = [
            'id', 'name', 'email', 'phone', 'company_name',
            'customer_type', 'status', 'address_line1', 'address_line2',
            'city', 'state', 'postal_code', 'country', 'billing_email',
            'tax_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SubscriptionSerializer(serializers.ModelSerializer):
    """Serializer for Subscription model"""
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    effective_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'customer', 'plan', 'customer_name', 'plan_name',
            'status', 'start_date', 'end_date', 'trial_end_date',
            'custom_price', 'discount_percentage', 'effective_price',
            'current_loan_applications', 'current_users', 'current_storage_gb',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'effective_price']


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice model"""
    customer_name = serializers.CharField(source='subscription.customer.name', read_only=True)
    plan_name = serializers.CharField(source='subscription.plan.name', read_only=True)
    subscription_id = serializers.CharField(source='subscription.id', read_only=True)
    
    class Meta:
        model = Invoice
        fields = [
            'id', 'subscription', 'subscription_id', 'invoice_number',
            'status', 'issue_date', 'due_date', 'paid_date',
            'subtotal', 'tax_amount', 'discount_amount', 'total_amount',
            'notes', 'customer_name', 'plan_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class PricingSettingsSerializer(serializers.ModelSerializer):
    """Serializer for PricingSettings model"""
    trial_plan_name = serializers.CharField(source='trial_plan.name', read_only=True)
    
    class Meta:
        model = PricingSettings
        fields = [
            'id', 'default_currency', 'tax_rate', 'trial_days',
            'trial_plan', 'trial_plan_name', 'invoice_prefix',
            'invoice_notes', 'payment_terms_days', 'allow_custom_pricing',
            'require_approval_for_custom', 'auto_renewal',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AuditLogSerializer(serializers.ModelSerializer):
    """Serializer for AuditLog model"""
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    plan_name = serializers.CharField(source='plan.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'action_type', 'description', 'plan', 'plan_name',
            'customer', 'customer_name', 'subscription', 'invoice',
            'changes', 'timestamp', 'user', 'user_name', 'ip_address'
        ]
        read_only_fields = ['id', 'timestamp']


# Dashboard-specific serializers
class PricingDashboardSerializer(serializers.Serializer):
    """Serializer for pricing dashboard data"""
    total_customers = serializers.IntegerField()
    active_subscriptions = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    pending_invoices = serializers.IntegerField()
    overdue_invoices = serializers.IntegerField()
    trial_subscriptions = serializers.IntegerField()
    popular_plan = serializers.CharField()
    revenue_by_plan = serializers.DictField()
    monthly_revenue_trend = serializers.ListField()


class PlanComparisonSerializer(serializers.Serializer):
    """Serializer for plan comparison data"""
    plan_id = serializers.UUIDField()
    plan_name = serializers.CharField()
    base_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    monthly_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    features = serializers.DictField()
    limits = serializers.DictField()
    is_featured = serializers.BooleanField()
    subscription_count = serializers.IntegerField()


class CustomerAnalyticsSerializer(serializers.Serializer):
    """Serializer for customer analytics data"""
    customer_id = serializers.UUIDField()
    customer_name = serializers.CharField()
    subscription_status = serializers.CharField()
    plan_name = serializers.CharField()
    effective_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    usage_percentage = serializers.FloatField()
    last_payment_date = serializers.DateTimeField()
    total_paid = serializers.DecimalField(max_digits=10, decimal_places=2)
    churn_risk = serializers.CharField()


# Nested serializers for detailed views
class DetailedPricingPlanSerializer(PricingPlanSerializer):
    """Detailed serializer for PricingPlan with related data"""
    subscriptions = SubscriptionSerializer(many=True, read_only=True)
    subscription_count = serializers.SerializerMethodField()
    
    def get_subscription_count(self, obj):
        return obj.subscriptions.count()


class DetailedCustomerSerializer(CustomerSerializer):
    """Detailed serializer for Customer with related data"""
    subscriptions = SubscriptionSerializer(many=True, read_only=True)
    active_subscriptions = serializers.SerializerMethodField()
    total_spent = serializers.SerializerMethodField()
    
    def get_active_subscriptions(self, obj):
        return obj.subscriptions.filter(status='active').count()
    
    def get_total_spent(self, obj):
        total = Decimal('0.00')
        for subscription in obj.subscriptions.all():
            for invoice in subscription.invoices.filter(status='paid'):
                total += invoice.total_amount
        return total


class DetailedSubscriptionSerializer(SubscriptionSerializer):
    """Detailed serializer for Subscription with related data"""
    customer = CustomerSerializer(read_only=True)
    plan = PricingPlanSerializer(read_only=True)
    invoices = InvoiceSerializer(many=True, read_only=True)
    usage_percentage = serializers.SerializerMethodField()
    
    def get_usage_percentage(self, obj):
        if obj.plan.max_loan_applications > 0:
            return (obj.current_loan_applications / obj.plan.max_loan_applications) * 100
        return 0
