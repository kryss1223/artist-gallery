#!/bin/sh
set -e

# Run migrations (safe for demo; no-op if already applied)
python manage.py migrate --noinput

# Collect static (needed for admin CSS etc.)
python manage.py collectstatic --noinput

# One-time superuser bootstrap (for demos)
if [ "${CREATE_SUPERUSER:-0}" = "1" ]; then
  echo "CREATE_SUPERUSER=1 -> ensuring superuser exists..."

  python manage.py shell -c "
import os
from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not username or not password:
    raise SystemExit('Missing DJANGO_SUPERUSER_USERNAME or DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superuser created:', username)
else:
    print('Superuser already exists:', username)
"
fi

# Start gunicorn on Render's port
exec gunicorn hello_django.wsgi:application --bind 0.0.0.0:${PORT:-8000}