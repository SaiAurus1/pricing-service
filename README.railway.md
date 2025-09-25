# Pricing Service - Railway Deployment

This is a standalone Django microservice for pricing functionality that will be deployed on Railway and later merged into the main docAnalysis repository.

## 🏗️ Architecture

```
Main docAnalysis Service ←→ Pricing Service
     (docAnalysis)              (this service)
         ↓                        ↓
    Railway Postgres ←→ Shared Database
```

## 📁 Project Structure

```
pricing-service/
├── pricing/                    # Main pricing app
│   ├── models.py              # PricingPlan, Customer, Subscription, etc.
│   ├── views.py               # API endpoints
│   ├── serializers.py         # DRF serializers
│   └── urls.py                 # API routes
├── pricing_service/           # Django project settings
│   ├── settings.py            # Local development settings
│   └── settings_railway.py   # Railway production settings
├── integration_client.py      # HTTP client for main service
├── Dockerfile.railway         # Production Dockerfile
├── railway.json               # Railway configuration
├── Procfile                   # Railway startup command
├── requirements.railway.txt   # Production dependencies
└── railway.env                # Environment variables template
```

## 🚀 Railway Deployment Steps

### 1. Create New Repository
```bash
# Create new repository for pricing service
git init
git add .
git commit -m "Initial pricing service setup"
git remote add origin <your-new-repo-url>
git push -u origin main
```

### 2. Railway Setup
1. Go to [Railway](https://railway.app)
2. Create new project
3. Connect your GitHub repository
4. Add PostgreSQL database service
5. Configure environment variables

### 3. Environment Variables
Set these in Railway dashboard:

```env
# Database
DB_NAME=your_railway_postgres_db_name
DB_USER=your_railway_postgres_user
DB_PASSWORD=your_railway_postgres_password
DB_HOST=your_railway_postgres_host
DB_PORT=5432

# Django
DJANGO_SECRET_KEY=your-secure-secret-key-here
DEBUG=False

# CORS (allow main docAnalysis service)
CORS_ALLOWED_ORIGINS=https://docanalysis-staging.up.railway.app,https://docanalysis-production.up.railway.app,https://myloan-stg.aurus.ai
```

### 4. Deploy
Railway will automatically:
- Build the Docker container
- Run migrations
- Start the service with gunicorn

## 🔗 API Endpoints

Once deployed, the service will be available at:
- **Base URL**: `https://your-pricing-service.up.railway.app`
- **API Root**: `https://your-pricing-service.up.railway.app/api/`

### Available Endpoints:
- `GET /api/plans/` - List pricing plans
- `POST /api/plans/` - Create pricing plan
- `GET /api/customers/` - List customers
- `POST /api/customers/` - Create customer
- `GET /api/subscriptions/` - List subscriptions
- `POST /api/subscriptions/` - Create subscription
- `GET /api/invoices/` - List invoices
- `POST /api/invoices/` - Create invoice
- `GET /api/settings/` - Pricing settings
- `GET /api/audit-logs/` - Audit logs
- `GET /api/dashboard/` - Dashboard data

## 🔄 Integration with Main Service

The pricing service is designed to integrate with the main docAnalysis service:

### 1. HTTP Client Integration
Use `integration_client.py` to communicate with the main service:

```python
from integration_client import DocAnalysisClient

client = DocAnalysisClient(base_url="https://docanalysis-staging.up.railway.app")
response = client.get_user_data(user_id=123)
```

### 2. Shared Database
Both services can access the same Railway PostgreSQL database for shared data.

### 3. CORS Configuration
The pricing service is configured to accept requests from:
- `https://docanalysis-staging.up.railway.app`
- `https://docanalysis-production.up.railway.app`
- `https://myloan-stg.aurus.ai` (DoKrunch Frontend)

## 🧪 Testing

### Local Testing
```bash
# Install dependencies
pip install -r requirements.railway.txt

# Set environment variables
export DJANGO_SECRET_KEY="your-secret-key"
export DEBUG=True

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### API Testing
```bash
# Test API endpoints
curl https://your-pricing-service.up.railway.app/api/plans/
curl https://your-pricing-service.up.railway.app/api/dashboard/
```

## 📋 Production Checklist

- [ ] Environment variables set in Railway
- [ ] PostgreSQL database connected
- [ ] CORS origins configured
- [ ] Secret key is secure
- [ ] DEBUG=False in production
- [ ] Static files collected
- [ ] Migrations run successfully
- [ ] Health check endpoint working
- [ ] Integration with main service tested

## 🔄 Future Integration

Once the pricing service is tested and working:

1. **Merge into main repository**: Move pricing app to main docAnalysis repo
2. **Update main service**: Add pricing endpoints to main service
3. **Database migration**: Move pricing tables to main database
4. **Remove standalone service**: Decommission Railway pricing service

## 📞 Support

This service is part of the docAnalysis ecosystem and will be maintained as part of the main project once integrated.

---

**Note**: This is a temporary standalone service for testing the pricing functionality before merging into the main docAnalysis repository.
