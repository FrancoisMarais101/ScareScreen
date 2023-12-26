# app.py
from flask import Flask
from extensions import db

from models.database import *  # Import models to ensure they are registered with SQLAlchemy
from os import environ


def create_app():
    app = Flask(__name__)

    # Fetching the Database connection parameters from the environment
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_PORT = environ.get("DB_PORT")
    DB_NAME = environ.get("DB_NAME")

    # Creating the SQLAlchemy engine
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Configure your app, including database URI and any other settings
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
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
