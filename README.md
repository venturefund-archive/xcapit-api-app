[![Coverage Status](https://coveralls.io/repos/gitlab/xcapit-foss/api-app/badge.svg?branch=HEAD)](https://coveralls.io/gitlab/xcapit-foss/api-app?branch=HEAD)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/0fa5ce637a384f37b41136d82022f3f6)](https://www.codacy.com/gl/xcapit-foss/api-app/dashboard?utm_source=gitlab.com&amp;utm_medium=referral&amp;utm_content=xcapit-foss/api-app&amp;utm_campaign=Badge_Grade)
# Xcapit Auth Service

Xcapit Auth Service is a rest api that manage all user related data. 

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
docker-compose exec <YOUR_HOST_HERE> psql -U <YOUR_USER_HERE>
CREATE DATABASE <YOUR_DB_NAME_HERE>
```

### Making db migrations

```sh
docker-compose exec api-app python manage.py makemigrations 
docker-compose exec api-app python manage.py migrate
```

Now in http://localhost:9070/ you can see the api.

## Tests (pytest)

To run the tests:

```sh
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
POSTGRES_HOST=<YOUR_HOST_HERE>
POSTGRES_PORT=<YOUR_PORT_HERE>
DJANGO_LOG_LEVEL=INFO

# APIs
API_NOTIFICATIONS=http://localhost:9051/v1/api/

# OTHERS
PWA_DOMAIN=http://localhost:8100/

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
      - 9070:9070
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

## Related Services

Xcapit Auth Service depends on backend services for send notifications. 

### Schema

The next schema represent Xcapit Auth Service interaction with services.

![smart wallet services relation](https://gitlab.com/xcapit-foss/documentation/-/raw/main/static/img/smart_wallet/XcapitSmartWallet_services_interaction.jpeg)
