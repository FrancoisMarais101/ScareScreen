# app.py
from os import environ
from flask import Flask
from extensions import db

from models.database import *  # Import models to ensure they are registered with SQLAlchemy


def create_app():
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
