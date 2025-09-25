"""
HTTP client for integrating with the main docAnalysis service.
This can be used in your main service to call the pricing service.
"""

import requests
import os
from typing import Dict, List, Optional
from decimal import Decimal


class PricingServiceClient:
    """Client for communicating with the pricing service"""
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv('PRICING_SERVICE_URL', 'https://pricing-service.up.railway.app')
        self.session = requests.Session()
        
        # Add authentication headers if needed
        auth_token = os.getenv('PRICING_SERVICE_TOKEN')
        if auth_token:
            self.session.headers.update({'Authorization': f'Bearer {auth_token}'})
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make HTTP request to pricing service"""
        url = f"{self.base_url}/api/{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    
    # Pricing Plans
    def get_plans(self) -> List[Dict]:
        """Get all pricing plans"""
        return self._make_request('GET', 'plans/')
    
    def get_active_plans(self) -> List[Dict]:
        """Get active pricing plans"""
        return self._make_request('GET', 'plans/active/')
    
    def get_featured_plans(self) -> List[Dict]:
        """Get featured pricing plans"""
        return self._make_request('GET', 'plans/featured/')
    
    def get_plan(self, plan_id: str) -> Dict:
        """Get specific pricing plan"""
        return self._make_request('GET', f'plans/{plan_id}/')
    
    def create_plan(self, data: Dict) -> Dict:
        """Create new pricing plan"""
        return self._make_request('POST', 'plans/', json=data)
    
    def update_plan(self, plan_id: str, data: Dict) -> Dict:
        """Update pricing plan"""
        return self._make_request('PUT', f'plans/{plan_id}/', json=data)
    
    def delete_plan(self, plan_id: str) -> None:
        """Delete pricing plan"""
        self._make_request('DELETE', f'plans/{plan_id}/')
    
    # Customers
    def get_customers(self) -> List[Dict]:
        """Get all customers"""
        return self._make_request('GET', 'customers/')
    
    def get_active_customers(self) -> List[Dict]:
        """Get active customers"""
        return self._make_request('GET', 'customers/active/')
    
    def get_customer(self, customer_id: str) -> Dict:
        """Get specific customer"""
        return self._make_request('GET', f'customers/{customer_id}/')
    
    def create_customer(self, data: Dict) -> Dict:
        """Create new customer"""
        return self._make_request('POST', 'customers/', json=data)
    
    def update_customer(self, customer_id: str, data: Dict) -> Dict:
        """Update customer"""
        return self._make_request('PUT', f'customers/{customer_id}/', json=data)
    
    def delete_customer(self, customer_id: str) -> None:
        """Delete customer"""
        self._make_request('DELETE', f'customers/{customer_id}/')
    
    # Subscriptions
    def get_subscriptions(self) -> List[Dict]:
        """Get all subscriptions"""
        return self._make_request('GET', 'subscriptions/')
    
    def get_active_subscriptions(self) -> List[Dict]:
        """Get active subscriptions"""
        return self._make_request('GET', 'subscriptions/active/')
    
    def get_subscription(self, subscription_id: str) -> Dict:
        """Get specific subscription"""
        return self._make_request('GET', f'subscriptions/{subscription_id}/')
    
    def create_subscription(self, data: Dict) -> Dict:
        """Create new subscription"""
        return self._make_request('POST', 'subscriptions/', json=data)
    
    def update_subscription(self, subscription_id: str, data: Dict) -> Dict:
        """Update subscription"""
        return self._make_request('PUT', f'subscriptions/{subscription_id}/', json=data)
    
    def cancel_subscription(self, subscription_id: str) -> Dict:
        """Cancel subscription"""
        return self.update_subscription(subscription_id, {'status': 'cancelled'})
    
    # Invoices
    def get_invoices(self) -> List[Dict]:
        """Get all invoices"""
        return self._make_request('GET', 'invoices/')
    
    def get_pending_invoices(self) -> List[Dict]:
        """Get pending invoices"""
        return self._make_request('GET', 'invoices/pending/')
    
    def get_invoice(self, invoice_id: str) -> Dict:
        """Get specific invoice"""
        return self._make_request('GET', f'invoices/{invoice_id}/')
    
    def create_invoice(self, data: Dict) -> Dict:
        """Create new invoice"""
        return self._make_request('POST', 'invoices/', json=data)
    
    def mark_invoice_paid(self, invoice_id: str) -> Dict:
        """Mark invoice as paid"""
        return self._make_request('PUT', f'invoices/{invoice_id}/', json={'status': 'paid'})
    
    # Dashboard
    def get_dashboard_data(self) -> Dict:
        """Get pricing dashboard data"""
        return self._make_request('GET', 'dashboard/')
    
    # Settings
    def get_settings(self) -> Dict:
        """Get pricing settings"""
        return self._make_request('GET', 'settings/')
    
    def update_settings(self, data: Dict) -> Dict:
        """Update pricing settings"""
        return self._make_request('PUT', 'settings/', json=data)


# Example usage in your main docAnalysis service
def example_integration():
    """Example of how to use the pricing service client"""
    
    # Initialize client
    pricing_client = PricingServiceClient()
    
    # Get all active pricing plans
    plans = pricing_client.get_active_plans()
    print(f"Found {len(plans)} active plans")
    
    # Create a new customer
    customer_data = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'customer_type': 'business',
        'company_name': 'Acme Corp'
    }
    customer = pricing_client.create_customer(customer_data)
    print(f"Created customer: {customer['id']}")
    
    # Create a subscription
    subscription_data = {
        'customer': customer['id'],
        'plan': plans[0]['id'],  # Use first available plan
        'start_date': '2024-01-01T00:00:00Z'
    }
    subscription = pricing_client.create_subscription(subscription_data)
    print(f"Created subscription: {subscription['id']}")
    
    # Get dashboard data
    dashboard = pricing_client.get_dashboard_data()
    print(f"Total customers: {dashboard['total_customers']}")
    print(f"Total revenue: {dashboard['total_revenue']}")


if __name__ == '__main__':
    example_integration()
