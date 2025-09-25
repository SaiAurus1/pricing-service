from django.contrib import admin
from .models import (
    PricingPlan, Customer, Subscription, Invoice,
    PricingSettings, AuditLog
)


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'base_price', 'billing_cycle', 'is_active', 'is_featured']
    list_filter = ['plan_type', 'billing_cycle', 'is_active', 'is_featured']
    search_fields = ['name', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'customer_type', 'status', 'created_at']
    list_filter = ['customer_type', 'status', 'created_at']
    search_fields = ['name', 'email', 'company_name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'plan', 'status', 'start_date', 'effective_price']
    list_filter = ['status', 'start_date', 'plan__plan_type']
    search_fields = ['customer__name', 'plan__name']
    readonly_fields = ['id', 'created_at', 'updated_at', 'effective_price']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'subscription', 'status', 'total_amount', 'due_date']
    list_filter = ['status', 'issue_date', 'due_date']
    search_fields = ['invoice_number', 'subscription__customer__name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(PricingSettings)
class PricingSettingsAdmin(admin.ModelAdmin):
    list_display = ['default_currency', 'tax_rate', 'trial_days', 'auto_renewal']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['action_type', 'description', 'timestamp', 'user']
    list_filter = ['action_type', 'timestamp']
    search_fields = ['description', 'user__username']
    readonly_fields = ['id', 'timestamp']
