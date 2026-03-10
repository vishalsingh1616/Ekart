# 🛒 Ekart — E-Commerce REST API

A full-featured e-commerce REST API built with Django REST Framework, JWT authentication, Redis caching, and Celery background tasks.

## 🚀 Tech Stack

- Python / Django 5 + Django REST Framework
- JWT Authentication (Simple JWT + Djoser)
- PostgreSQL / SQLite
- Redis (caching + Celery broker)
- django-filter for advanced filtering

## ⚙️ Local Setup
```bash
# 1. Clone the repo
git clone https://github.com/your-username/Ekart.git
cd Ekart

# 2. Install dependencies
pip install -r requirements.txt

# 3. Apply migrations
python manage.py migrate

# 4. Create a superuser (admin)
python manage.py createsuperuser

# 5. Start the server
python manage.py runserver
```

> Redis must be running for caching and Celery to work: `redis-server`

## ✨ Features

- Product listing with search, filtering, and ordering
- Collection management
- Shopping cart (anonymous, UUID-based)
- Order placement from cart
- Customer profiles with membership tiers
- Product image uploads
- Product reviews
- JWT-based authentication and registration

## 📄 Documentation

See the [Full API Documentation](docs/ekart_api_docs.pdf) for all endpoints, request/response fields, and example workflows.

## 📬 API Base URL
```
http://localhost:8000
```

Authentication: `Authorization: JWT <your_token>`
