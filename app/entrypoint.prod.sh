#!/bin/sh
set -e

# Run migrations (safe for demo; no-op if already applied)
python manage.py migrate --noinput

# Collect static (needed for admin CSS etc.)
python manage.py collectstatic --noinput

# Start gunicorn on Render's port
exec gunicorn hello_django.wsgi:application --bind 0.0.0.0:${PORT:-8000}