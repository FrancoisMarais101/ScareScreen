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
from flask import Flask, jsonify, request
from sqlalchemy.exc import SQLAlchemyError
from extensions import db
from flask_cors import CORS
import requests
from googleapiclient.discovery import build
import datetime


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

    CORS(app)

    # Fetching the Database connection parameters from the environment
    db_user = environ.get("db_user")
    db_pass = environ.get("db_pass")
    db_host = environ.get("db_host")
    db_port = environ.get("db_port")
    db_name = environ.get("db_name")
    youtube_api_key = environ.get("youtube_api_key")

    # Creating the SQLAlchemy engine
    database_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # Configure your app, including database URI and any other settings
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize plugins
    db.init_app(app)

    # YouTube API setup

    # youtube = build("youtube", "v3", developerKey=youtube_api_key)

    # def search_trailers():
    #     request = youtube.search().list(
    #         q="horror movie trailer",
    #         part="snippet",
    #         type="video",
    #         publishedAfter=f"{datetime.datetime.now().year}-01-01T00:00:00Z",
    #         maxResults=50,
    #     )
    #     response = request.execute()

    #     for item in response["items"]:
    #         add_trailer(item)

    # def add_trailer(item):
    #     # Extracting necessary data from the item
    #     title = item["snippet"]["title"]
    #     url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"

    #     # Similar to add_the_witch, but for each trailer
    #     db.session.rollback()

    #     new_trailer = Trailer(url=url)  # Assuming Trailer model has a URL field
    #     # Create a Trailer
    #     # the_witch_trailer = Trailer(url="https://www.youtube.com/watch?v=iQXmlf3Sefg")
    #     db.session.add(new_trailer)

    #     # Commit the session to ensure 'youtube' and 'the_witch_trailer' have 'id' populated
    #     db.session.commit()

    #     # Create a PlatformTrailer association
    #     # the_witch_platform_trailer = PlatformTrailer(
    #     #     trailer_id=the_witch_trailer.id, platform_id=youtube.id
    #     # )
    #     # db.session.add(the_witch_platform_trailer)

    #     # Create an instance of the Movie class with The Witch details
    #     new_movieh = Movie(
    #         title=title,
    #     )

    #     try:
    #         db.session.add(new_movieh)
    #         db.session.commit()
    #         return jsonify(message="The Witch added successfully"), 201
    #     except SQLAlchemyError as e:
    #         db.session.rollback()
    #         error_info = str(e.__dict__.get("orig", e))  # Safer access to 'orig'
    #         return jsonify(error=error_info), 400

    # Define routes
    @app.route("/")
    def hello_world():
        return "Hello, World! This is the home page."

    # @app.route("/search_trailers", methods=["POST"])
    # def trigger_search():
    #     # Maybe include some authentication to protect this endpoint
    #     search_trailers()
    #     return jsonify({"message": "Search initiated"}), 200

    @app.route("/api/movies", methods=["GET"])
    def get_movies():
        try:
            movies = Movie.query.all()
            movies_list = [
                {
                    "id": movie.id,
                    "title": movie.title,
                    "director": movie.director,
                    "cast": movie.cast,
                    "release_date": movie.release_date,
                    "length": movie.length,
                    "rating": movie.rating,
                    "age_restriction": movie.age_restriction,
                    "summary": movie.summary,
                }
                for movie in movies
            ]
            return jsonify(movies_list), 200
        except SQLAlchemyError as e:
            app.logger.error(f"Error fetching movies: {e}")
            return jsonify(error="An error occurred fetching movies"), 500

    @app.route("/add_the_witch", methods=["POST"])
    def add_the_witch():
        # Ensuring the session is fresh
        db.session.rollback()

        # Check for existing StreamingPlatform or create a new one
        youtube = StreamingPlatform.query.filter_by(name="Youtube").first()
        if not youtube:
            youtube = StreamingPlatform(name="Youtube")
            db.session.add(youtube)

        # Create a Trailer
        the_witch_trailer = Trailer(url="https://www.youtube.com/watch?v=iQXmlf3Sefg")
        db.session.add(the_witch_trailer)

        # Commit the session to ensure 'youtube' and 'the_witch_trailer' have 'id' populated
        db.session.commit()

        # Create a PlatformTrailer association
        the_witch_platform_trailer = PlatformTrailer(
            trailer_id=the_witch_trailer.id, platform_id=youtube.id
        )
        db.session.add(the_witch_platform_trailer)

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

    # @app.route("/add_movie", methods=["POST"])
    # def add_movie():
    #     # Getting movie data from the request body
    #     movie_data = request.json

    #     db.session.rollback()

    #     # The rest remains largely the same, but use 'movie_data' to provide values
    #     new_movie = Movie(
    #         title=movie_data.get("title"),
    #         director=movie_data.get("director"),
    #         cast=movie_data.get("cast"),
    #         release_date=movie_data.get("release_date"),
    #         length=movie_data.get("length"),
    #         rating=movie_data.get("rating"),
    #         age_restriction=movie_data.get("age_restriction"),
    #         summary=movie_data.get("summary"),
    #     )

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="localhost", port=8000)
