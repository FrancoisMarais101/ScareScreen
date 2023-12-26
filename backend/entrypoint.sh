#!/bin/bash

# Make sure to stop the script if any command fails
set -e

# Wait for the database to be ready
echo "Waiting for DB to be ready..."
/backend/wait-for-db.sh db

# Initialize the database and create tables
echo "Initializing the database..."
python /backend/init_db.py

# Start the main application
echo "Starting the application with Gunicorn..."
gunicorn "app:create_app()"
