# API APP

# Version: v0.0.0

`docker-compose exec postgres-api-app psql -U postgres`

`CREATE DATABASE api_app_db`

Salir del container (Ctrl+D)

Migrar la db

`docker-compose exec api-app python manage.py makemigrations administration profiles referrals stats terms_and_conditions users`

`docker-compose exec api-app python manage.py migrate`