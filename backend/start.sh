#!/bin/sh

# This script waits for the dependencies to be available before starting the app.

set -e

# Wait for PostgreSQL
echo "Waiting for PostgreSQL..."
while ! nc -z todo-db 5432; do
  sleep 0.1
done
echo "PostgreSQL started"

# Wait for Redis
echo "Waiting for Redis..."
while ! nc -z todo-redis 6379; do
  sleep 0.1
done
echo "Redis started"

# Wait for RabbitMQ
echo "Waiting for RabbitMQ..."
while ! nc -z todo-rabbitmq 5672; do
  sleep 0.1
done
echo "RabbitMQ started"

# Execute the main application
echo "All dependencies started. Starting the application..."
exec python app.py
