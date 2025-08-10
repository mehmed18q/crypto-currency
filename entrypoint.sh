#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Fetching initial prices..."
python manage.py fetch_prices || true

export DJANGO_SETTINGS_MODULE=crypto_price.settings
#pytest

exec "$@"
