#!/bin/bash

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

# Set Python path to include the current directory
export PYTHONPATH=/app

# Run migrations
echo "Running migrations..."
python -m app.migrations.create_user_project_tables

# Start the application
echo "Starting application..."
uvicorn app.main:app --host 0.0.0.0 --port 5001
