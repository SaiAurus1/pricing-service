from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
import uuid


class PricingPlan(models.Model):
    """Pricing plans for different subscription tiers"""
    
    PLAN_TYPES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
        ('custom', 'Custom'),
    ]
    
    BILLING_CYCLES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
        ('lifetime', 'Lifetime'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    billing_cycle = models.CharField(max_length=20, choices=BILLING_CYCLES, default='monthly')
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    setup_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    
    # Features and limits
    max_loan_applications = models.PositiveIntegerField(default=100)
    max_users = models.PositiveIntegerField(default=5)
    max_storage_gb = models.PositiveIntegerField(default=10)
    
    # Feature flags
    api_access = models.BooleanField(default=False)
    advanced_analytics = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    white_label = models.BooleanField(default=False)
    custom_integrations = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_plans')
    
    class Meta:
        ordering = ['base_price', 'name']
        verbose_name = "Pricing Plan"
        verbose_name_plural = "Pricing Plans"
    
    def __str__(self):
        return f"{self.name} ({self.get_plan_type_display()})"
    
    @property
    def monthly_price(self):
        """Calculate monthly equivalent price"""
        if self.billing_cycle == 'monthly':
            return self.base_price
        elif self.billing_cycle == 'quarterly':
            return self.base_price / 3
        elif self.billing_cycle == 'yearly':
            return self.base_price / 12
        else:  # lifetime
            return self.base_price / 120  # Assuming 10 years lifetime


class Customer(models.Model):
    """Customer/Client information for pricing"""
    
    CUSTOMER_TYPES = [
        ('individual', 'Individual'),
        ('business', 'Business'),
        ('enterprise', 'Enterprise'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200, blank=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='individual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Address
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    
    # Billing
    billing_email = models.EmailField(blank=True)
    tax_id = models.CharField(max_length=50, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_customers')
    
    class Meta:
        ordering = ['name']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
    
    def __str__(self):
        return f"{self.name} ({self.email})"


class Subscription(models.Model):
    """Customer subscriptions to pricing plans"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('trial', 'Trial'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(PricingPlan, on_delete=models.CASCADE, related_name='subscriptions')
    
    # Subscription details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trial')
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    trial_end_date = models.DateTimeField(null=True, blank=True)
    
    # Pricing
    custom_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))])
    
    # Usage tracking
    current_loan_applications = models.PositiveIntegerField(default=0)
    current_users = models.PositiveIntegerField(default=0)
    current_storage_gb = models.PositiveIntegerField(default=0)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_subscriptions')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
    
    def __str__(self):
        return f"{self.customer.name} - {self.plan.name}"
    
    @property
    def effective_price(self):
        """Calculate effective price after discounts"""
        price = self.custom_price or self.plan.base_price
        if self.discount_percentage > 0:
            discount_amount = price * (self.discount_percentage / 100)
            return price - discount_amount
        return price


class Invoice(models.Model):
    """Invoices for subscriptions"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    
    # Invoice details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    issue_date = models.DateTimeField()
    due_date = models.DateTimeField()
    paid_date = models.DateTimeField(null=True, blank=True)
    
    # Amounts
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Notes
    notes = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_invoices')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.subscription.customer.name}"


class PricingSettings(models.Model):
    """Global pricing settings and configuration"""
    
    CURRENCY_CHOICES = [
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
        ('CAD', 'Canadian Dollar'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # General settings
    default_currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='USD')
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))])
    
    # Trial settings
    trial_days = models.PositiveIntegerField(default=14)
    trial_plan = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='trial_settings')
    
    # Billing settings
    invoice_prefix = models.CharField(max_length=10, default='INV')
    invoice_notes = models.TextField(blank=True)
    payment_terms_days = models.PositiveIntegerField(default=30)
    
    # Feature settings
    allow_custom_pricing = models.BooleanField(default=True)
    require_approval_for_custom = models.BooleanField(default=True)
    auto_renewal = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='updated_pricing_settings')
    
    class Meta:
        verbose_name = "Pricing Settings"
        verbose_name_plural = "Pricing Settings"
    
    def __str__(self):
        return "Pricing Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and PricingSettings.objects.exists():
            raise ValueError("Only one PricingSettings instance is allowed")
        super().save(*args, **kwargs)


class AuditLog(models.Model):
    """Audit logs for pricing-related actions"""
    
    ACTION_TYPES = [
        ('plan_created', 'Plan Created'),
        ('plan_updated', 'Plan Updated'),
        ('plan_deleted', 'Plan Deleted'),
        ('subscription_created', 'Subscription Created'),
        ('subscription_updated', 'Subscription Updated'),
        ('subscription_cancelled', 'Subscription Cancelled'),
        ('invoice_created', 'Invoice Created'),
        ('invoice_paid', 'Invoice Paid'),
        ('customer_created', 'Customer Created'),
        ('customer_updated', 'Customer Updated'),
        ('settings_updated', 'Settings Updated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Action details
    action_type = models.CharField(max_length=30, choices=ACTION_TYPES)
    description = models.TextField()
    
    # Related objects
    plan = models.ForeignKey(PricingPlan, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    
    # Changes (JSON field to store before/after values)
    changes = models.JSONField(null=True, blank=True)
    
    # Metadata
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='pricing_audit_logs')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
    
    def __str__(self):
        return f"{self.get_action_type_display()} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
