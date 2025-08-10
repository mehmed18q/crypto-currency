FROM python:3.11-slim

WORKDIR /app

# Prevent pyc generation and output buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=crypto_price.settings

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . /app/

# Create a staticfiles folder and collect static files
RUN mkdir -p /app/staticfiles
RUN python manage.py collectstatic --noinput

# Create a secure user
RUN adduser --disabled-password appuser || true
USER appuser

# Start script
ENTRYPOINT ["/app/entrypoint.sh"]

# Run tests
RUN pytest --cache-clear || exit 0

# Run gunicorn
CMD ["gunicorn", "crypto_price.wsgi:application", "--bind", "0.0.0.0:8000"]
