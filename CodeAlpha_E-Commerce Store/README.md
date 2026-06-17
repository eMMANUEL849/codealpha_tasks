# UrbanCart — Django Store

Simple Django ecommerce example adapted for clarity and maintainability.

What's included
- Minimal product, cart and order models
- Basic user registration and login
- Admin dashboard plus Django admin

Quick start

1. Create a virtualenv and install dependencies

```bash
python -m venv venv
venv\\Scripts\\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Notes
- This repo is organized for readability and quick iteration. Run linters and tests as needed.
