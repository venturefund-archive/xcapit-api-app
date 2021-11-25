[![Coverage Status](https://coveralls.io/repos/gitlab/xcapit-foss/api-app/badge.svg?branch=develop)](https://coveralls.io/gitlab/xcapit-foss/api-app?branch=develop)

# Xcapit Auth Service

Xcapit Auth Service is a rest api that offers

## Getting Started

### Installation

Clone the repo and open the directory:

```sh
git clone https://gitlab.com/xcapit-foss/api-app auth-service
cd auth-service
```

Ensure you have [Docker](https://www.docker.com/) and [Docker compose](https://docs.docker.com/compose/install/)
installed, and [configuration files](#configuration), then:

```sh
docker-compose build
docker-compose up -d
```

### Creating a database

```sh
docker-compose exec postgres-api-app psql -U postgres
CREATE DATABASE mydb
```

### Making db migrations

```sh
docker-compose exec api-app python manage.py makemigrations administration profiles referrals stats terms_and_conditions users
docker-compose exec api-app python manage.py migrate
```

Now in http://localhost:9070/ you can see the api.

## Tests (pytest)

To run the tests:

```
 docker-compose exec api-app pytest
```

<h2 id="configuration">Configuration</h2>
For configuration settings you could see and change the next file.

```sh
./variables.env
./docker-compose.yml
```

### Example files

```dotenv
# variables.env
DEBUG=1
SECRET=<YOUR_SECRET_HERE>
POSTGRES_USER=<YOUR_USER_HERE>
POSTGRES_DB=<YOUR_DB_NAME_HERE>
POSTGRES_PASSWORD=<YOUR_PASS_HERE>
POSTGRES_HOST=postgres-api-app
POSTGRES_PORT=5432
DJANGO_LOG_LEVEL=INFO

# Postgres Exporter
DATA_SOURCE_URI=postgres-api-app:5432/mydb?sslmode=disable
DATA_SOURCE_USER=<YOUR_USER_HERE>
DATA_SOURCE_PASS=<YOUR_PASS_HERE>
PG_EXPORTER_AUTO_DISCOVER_DATABASES=true

# APIs
API_NOTIFICATIONS=http://localhost:9051/v1/api/

# OTHERS
PWA_DOMAIN=https://nonprod.xcapit.com

# Firebase clients
CLIENT_ID_1=<YOUR_FIREBASE_CLIENT_ID_1_HERE>
CLIENT_ID_2=<YOUR_FIREBASE_CLIENT_ID_2_HERE>
CLIENT_ID_3=<YOUR_FIREBASE_CLIENT_ID_3_HERE>

# Mercadopago
API_MERCADOPAGO=https://api.mercadopago.com/
MERCADOPAGO_ACCESS_TOKEN=<YOUR_MERCADOPAGO_ACCESS_TOKEN_HERE>
MERCADOPAGO_PUBLIC_KEY=<YOUR_MERCADOPAGO_PUBLIC_KEY_HERE>

SENTRY_HOST=<YOUR_SENTRY_HOST_HERE>
SENTRY_KEY=<YOUR_SENTRY_KEY_HERE>
```

```yaml
# docker-compose.yml
version: "3.2"
services:
  api-app:
    build: .
    volumes:
      - .:/code
    command: python3 manage.py runserver 9070
    ports:
      - 9070:8000
    env_file:
      - ./variables.env

  postgres-api-app:
    image: postgres:12.0
    volumes:
      - ./postgres:/var/lib/postgresql/data
    ports:
      - 5435:5432
    env_file:
      - ./variables.env
```

## Docker

You can run Xcapit Api App with [Docker](https://www.docker.com/) by running the following commands.

```sh
docker-compose up -d
```

## Related Services

Xcapit Auth Service depends on backend services for send notifications. 

### Schema

The next schema represent Xcapit Auth Service interaction with services.

![smart wallet services relation](https://gitlab.com/xcapit-foss/documentation/-/raw/main/static/img/smart_wallet/XcapitSmartWallet_services_interaction.jpeg)
