#!/bin/bash
# Deployment script for Lab Booking System

# Install dependencies
pip install -r requirements.txt

# Run migrations
python backened/manage.py migrate

# Collect static files
python backened/manage.py collectstatic --noinput

# Create superuser (optional, run manually)
# python backened/manage.py createsuperuser

# Run server (for development)
# python backened/manage.py runserver

# For production, use gunicorn or similar
# gunicorn lab_booking.wsgi:application --bind 0.0.0.0:8000
