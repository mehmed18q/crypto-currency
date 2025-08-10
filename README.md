# Crypto Prices Project

**Author:** Mohammad Sadeq Kiumarsi  
**Phone:** +989217074647  
**Email:** mehmed2002q@gmail.com

---

## Overview

Crypto Prices is a Django-based web service for fetching, storing, and serving cryptocurrency price data. It supports multiple data providers, scheduled background tasks, and a REST API with automatic documentation.

---

## Features

- Fetches cryptocurrency prices from configurable providers (e.g., CoinGecko, Binance)
- Stores price history in Sqlite database
- Provides REST API endpoints for latest prices and historical price data
- Manual and scheduled price fetching using Celery & Celery Beat
- Async background tasks for improved performance
- Admin panel for managing cryptocurrencies and price data
- Structured JSON responses including status, HTTP code, message, and data
- API documentation via Swagger (drf-yasg)
- Containerized with Docker & Docker Compose for easy deployment

---

## Technology Stack

- **Backend Framework:** Django 5.x
- **REST API:** Django REST Framework (DRF)
- **API Documentation:** drf-yasg (Swagger)
- **Task Queue:** Celery with Redis as broker
- **Scheduler:** Celery Beat for periodic tasks
- **Database:** Sqlite15
- **Cache / Broker:** Redis 7
- **Containerization:** Docker & Docker Compose
- **Python Version:** 3.11 (slim)
- **Async Support:** Async views and Celery async tasks for scalability

---

## Project Structure
/app

├── crypto_price/ # Django project settings and URLs

├── prices/ # App for cryptocurrency price models, views, serializers, and services

│ ├── management/commands/fetch_prices.py # Fetch current prices once (used by entrypoint or manually)

│ ├── providers/ # Price provider implementations (CoinGecko, Binance)

│ ├── services/ # Business logic for fetching and storing prices

│ ├── tests/ # Unit and integration tests

│ ├── admin.py # Django admin configuration

│ ├── models.py # DB models for Currency and PriceHistory

│ ├── serializers.py # Serializers for output

│ ├── tasks.py # Celery tasks

│ ├── urls.py # Url patterns

│ ├── utils.py # api response

│ └── view.py # endpoints 

├── Crypto-Currency.postman_collection.json # postman collection

├── requirements.txt # project requirements

├── docker-compose.yml

├── Dockerfile

└── entrypoint.sh # Entrypoint script for migrations and static files

---

## Setup and Installation

### Prerequisites

- Docker & Docker Compose installed
- Git installed
- (Optional) Python 3.11 for local dev without Docker

### Running with Docker Compose


git clone https://github.com/yourusername/crypto-prices.git
cd crypto-prices

# Build and start containers
```
docker compose up --build
```

This will start:

Sqlitedatabase on port 5432

Redis broker on port 6379

Django web app on port 8000

Celery worker and Celery Beat scheduler

API Endpoints
```
GET prices/latest/
```
Returns the latest prices of all active cryptocurrencies.

```
GET prices/history/{code}/?limit=N
````
Returns historical price data for the specified currency code with optional limit.

```
POST prices/fetch/
```
Triggers a manual fetch of the latest prices from the configured provider.

API Documentation:
```
/
```

Background Tasks
Periodic price fetching every 5 minutes using Celery Beat.

Tasks executed asynchronously by Celery workers.

Logs and errors properly handled and displayed.

Admin Panel
Accessible at /admin/.
Manage:

Cryptocurrencies (add/remove/activate/deactivate)

View price history entries

Configuration
Environment variables (set in docker-compose.yml or .env):

```
CELERY_BROKER_URL: Redis connection string

CRYPTO_PRICE_PROVIDER: Name of price provider to use (coingecko or binance)

DJANGO_DEBUG: Enable/disable debug mode (1 or 0)
```

### Testing
Run tests locally:

```
pytest
```

Tests cover:

Price fetching service

API endpoints

Celery task execution

### Contact
For questions, bug reports, or contributions, contact Mohammad Sadeq Kiumarsi at:

Email: mehmed2002q@gmail.com

Phone: +989217074647

Website: http://sadeqkiumarsi.ir

### License
This project is licensed under the FUT Plus License.

Thank you for using Crypto Prices Project!
