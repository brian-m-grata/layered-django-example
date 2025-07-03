#!/bin/bash

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "Database is ready!"

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Start Django
echo "Starting Django..."
python manage.py runserver 0.0.0.0:8000 