"""
app.py
------

A Flask application module for initializing and running a Flask web service.

This module contains the Flask application factory `create_app` which sets 
up the application with necessary configurations, initializes the database 
connection using Flask-SQLAlchemy, and defines the basic route for the application. 
The database models are imported to ensure they are registered with SQLAlchemy.

It fetches database configurations from the environment variables and sets up 
the SQLAlchemy connection to a PostgreSQL database.

The application defines a single route, the home page, which simply 
returns a "Hello, World!" message.

Attributes:
    db_user (str): Database username fetched from environment variables.
    db_pass (str): Database password fetched from environment variables.
    db_host (str): Database host fetched from environment variables.
    db_port (str): Database port fetched from environment variables.
    db_name (str): Database name fetched from environment variables.
    database_url (str): Full database connection URL constructed from the above credentials.
    app (Flask): The Flask application instance.
    flask_app (Flask): The Flask application instance when the script is run directly.

Functions:
    create_app(): Flask application factory function for setting up and returning a Flask app.

Usage:
    Run this file directly using Python to start the Flask application server:
    ```
    python app.py
    ```
"""
from os import environ
from flask import Flask
from extensions import db

from models.database import *  # Import models to ensure they are registered with SQLAlchemy


def create_app():
    """
    Creates and configures an instance of the Flask application.

    The Flask application is configured with the necessary database settings and routes. It fetches
    database connection parameters from the environment, constructs a database URL, and initializes the
    SQLAlchemy plugin with this app instance. It defines a simple route as an example.

    Returns:
        app: A Flask application instance with routes and configurations set up.

    Environment Variables:
        - db_user: Database username
        - db_pass: Database password
        - db_host: Database host address
        - db_port: Database port number
        - db_name: Database name

    Note:
        Ensure that all required environment variables are set before calling this function.
    """
    app = Flask(__name__)

    # Fetching the Database connection parameters from the environment
    db_user = environ.get("db_user")
    db_pass = environ.get("db_pass")
    db_host = environ.get("db_host")
    db_port = environ.get("db_port")
    db_name = environ.get("db_name")

    # Creating the SQLAlchemy engine
    database_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # Configure your app, including database URI and any other settings
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize plugins
    db.init_app(app)

    @app.route("/")
    def hello_world():
        return "Hello, World! This is the home page."

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=8000)
