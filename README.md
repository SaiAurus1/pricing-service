# Pricing Service

A standalone Django microservice for managing pricing plans, customers, subscriptions, and invoices.

## Features

- **Pricing Plans Management**: Create and manage different subscription tiers
- **Customer Management**: Handle customer information and billing details
- **Subscription Management**: Track customer subscriptions and usage
- **Invoice Generation**: Generate and manage invoices
- **Analytics Dashboard**: View pricing metrics and analytics
- **Audit Logging**: Track all pricing-related actions

## API Endpoints

### Pricing Plans
- `GET /api/plans/` - List all pricing plans
- `GET /api/plans/active/` - Get active pricing plans
- `GET /api/plans/featured/` - Get featured pricing plans
- `POST /api/plans/` - Create new pricing plan
- `GET /api/plans/{id}/` - Get specific pricing plan
- `PUT /api/plans/{id}/` - Update pricing plan
- `DELETE /api/plans/{id}/` - Delete pricing plan

### Customers
- `GET /api/customers/` - List all customers
- `GET /api/customers/active/` - Get active customers
- `POST /api/customers/` - Create new customer
- `GET /api/customers/{id}/` - Get specific customer
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

### Subscriptions
- `GET /api/subscriptions/` - List all subscriptions
- `GET /api/subscriptions/active/` - Get active subscriptions
- `POST /api/subscriptions/` - Create new subscription
- `GET /api/subscriptions/{id}/` - Get specific subscription
- `PUT /api/subscriptions/{id}/` - Update subscription
- `DELETE /api/subscriptions/{id}/` - Delete subscription

### Invoices
- `GET /api/invoices/` - List all invoices
- `GET /api/invoices/pending/` - Get pending invoices
- `POST /api/invoices/` - Create new invoice
- `GET /api/invoices/{id}/` - Get specific invoice
- `PUT /api/invoices/{id}/` - Update invoice

### Dashboard
- `GET /api/dashboard/` - Get pricing dashboard data

## Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

5. **Run development server**:
   ```bash
   python manage.py runserver
   ```

## Deployment

### Railway Deployment

1. **Create new service** in Railway dashboard
2. **Connect your repository**
3. **Set environment variables**:
   - `DB_NAME`: Your Railway Postgres database name
   - `DB_USER`: Your Railway Postgres username
   - `DB_PASSWORD`: Your Railway Postgres password
   - `DB_HOST`: Your Railway Postgres host
   - `DB_PORT`: 5432
   - `DJANGO_SECRET_KEY`: Your Django secret key
   - `DEBUG`: False

4. **Deploy**

### Docker Deployment

```bash
docker build -t pricing-service .
docker run -p 8000:8000 --env-file .env pricing-service
```

## Integration with Main Service

To integrate with your main docAnalysis service, add HTTP client calls:

```python
import requests

class PricingServiceClient:
    def __init__(self):
        self.base_url = os.getenv('PRICING_SERVICE_URL', 'https://pricing-service.up.railway.app')
    
    def get_plans(self):
        response = requests.get(f"{self.base_url}/api/plans/")
        return response.json()
    
    def create_subscription(self, data):
        response = requests.post(f"{self.base_url}/api/subscriptions/", json=data)
        return response.json()
```

## Database Schema

The service uses the same Postgres database as your main docAnalysis service, so all data is shared between services.

## Authentication

The service uses JWT authentication. Make sure to include the JWT token in your requests:

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" https://pricing-service.up.railway.app/api/plans/
```
