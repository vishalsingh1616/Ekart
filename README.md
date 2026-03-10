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

# 2. Create and activate virtual environment
python -m venv env

# On Windows
env\Scripts\activate

# On Mac/Linux
source env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser (admin)
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```
## 🧪 Testing the API

To test authenticated endpoints, you need to send the JWT token in the request header:
```
Authorization: JWT <your_access_token>
1. Install [ModHeader](https://modheader.com/) for Chrome or Firefox
2. Click the extension icon
3. Add a request header:
   - Name: `Authorization`
   - Value: `JWT <paste_token_here>`
4. Now all requests from your browser will include the token
```

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

> Redis must be running for caching and Celery to work: `redis-server`

## 📬 API Base URL
```
http://localhost:8000
```

Authentication: `Authorization: JWT <your_token>`
