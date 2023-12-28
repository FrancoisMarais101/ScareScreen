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
from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError
from extensions import db


# Import models to ensure they are registered with SQLAlchemy
from models.database import Movie  # pylint: disable=unused-import
from models.database import Trailer  # pylint: disable=unused-import
from models.database import StreamingPlatform  # pylint: disable=unused-import
from models.database import PlatformTrailer  # pylint: disable=unused-import
from models.database import User  # pylint: disable=unused-import
from models.database import Review  # pylint: disable=unused-import
from models.database import Recommendation  # pylint: disable=unused-import
from models.database import Notification  # pylint: disable=unused-import
from models.database import Watchlist  # pylint: disable=unused-import


def create_app():
    """
    Creates and configures an instance of the Flask application.

    The Flask application is configured with the necessary database
    settings and routes. It fetches database connection parameters
    from the environment, constructs a database URL, and initializes the
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

    @app.route("/add_the_witch", methods=["POST"])
    def add_the_witch():
        # Create an instance of the Movie class with The Witch details
        the_witch = Movie(
            title="The Witch",
            director="Robert Eggers",
            cast="Anya Taylor-Joy, Ralph Ineson, Kate Dickie, Harvey Scrimshaw",
            release_date="2015-01-27",  # Use the appropriate date format your DB expects
            length=92,  # Length in minutes
            rating=6.9,  # Just an example rating
            age_restriction=16,  # Just an example age restriction
            summary="A family in 1630s New England is torn apart by the forces of witchcraft, \
            black magic, and possession.",
        )

        try:
            db.session.add(the_witch)
            db.session.commit()
            return jsonify(message="The Witch added successfully"), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            error_info = str(e.__dict__.get("orig", e))  # Safer access to 'orig'
            return jsonify(error=error_info), 400
        # Consider catching other specific exceptions you expect might occur

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="localhost", port=8000)
