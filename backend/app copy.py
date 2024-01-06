"""
app.py
------

A Flask application module for initializing and running a web service.

This module contains the Flask application factory `create_app` which sets
up the application with necessary configurations, initializes the database
connection using Flask-SQLAlchemy, and defines routes for the application.
The database models are imported to ensure they are registered with SQLAlchemy.

It fetches database configurations from the environment variables and sets up
the SQLAlchemy connection to a PostgreSQL database.

The application defines multiple routes, including the home page, movie data retrieval,
and adding trailers to the database via interaction with the YouTube API.

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
    search_trailers(): Route function to fetch and add trailers from YouTube API.
    add_trailer(item): Helper function to add individual trailer to the database.
    hello_world(): Route function to serve the home page.
    get_movies(): Route function to fetch and return all movies from the database.

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
from flask_cors import CORS  # pylint: disable=import-error
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from requests.exceptions import (
    ConnectionError as RequestsConnectionError,
    Timeout,
    RequestException,
)

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

    Fetches database connection parameters from the environment, constructs a database URL,
    and initializes the SQLAlchemy plugin with this app instance. It defines routes for
    various operations including fetching movie data and adding new trailers.

    Returns:
        Flask: A Flask application instance with routes and configurations set up.

    Note:
        Ensure that all required environment variables are set before calling this function.
    """
    app = Flask(__name__)
    CORS(app)

    # Fetching Database connection parameters from the environment
    db_user = environ.get("db_user")
    db_pass = environ.get("db_pass")
    db_host = environ.get("db_host")
    db_port = environ.get("db_port")
    db_name = environ.get("db_name")
    youtube_api_key = environ.get("youtube_api_key")

    # Creating the SQLAlchemy engine
    database_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # Configure the app, including database URI and any other settings
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize plugins
    db.init_app(app)

    # YouTube API setup
    youtube = build("youtube", "v3", developerKey=youtube_api_key)

    def get_names():
        # Define the base URL and your API key
        base_url = "https://api.themoviedb.org/3"
        api_key = "YOUR_API_KEY"

        # Define the Discover endpoint with the horror genre ID
        endpoint = f"{base_url}/discover/movie?api_key={api_key}&with_genres=27"

        # Make the request
        response = requests.get(endpoint)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the response
            data = response.json()
            for movie in data["results"]:
                # Construct the full path for the poster image
                poster_path = "https://image.tmdb.org/t/p/w500" + movie["poster_path"]
                print(movie["title"], poster_path)

    def search_trailers(movie_name):
        """
        A function to fetch and add movie trailers from the YouTube API to the database.
        Searches for trailers published in the current year and adds them to the database.

        Returns:
            Response: A success or error response.
        """
        try:
            request = youtube.search().list(
                q=f"{movie_name} trailer",
                part="snippet",
                type="video",
                maxResults=1,  # Assuming you want only the most relevant result
            )
            response = request.execute()

            for item in response["items"]:
                add_trailer(item)

            return jsonify({"message": "Trailers added successfully"}), 200
        except HttpError as e:
            print(f"HTTP error occurred: {e}")
            return (
                jsonify({"error": "Failed to add trailers due to an HTTP error"}),
                500,
            )

        except RequestsConnectionError as e:
            # Handle connection errors specifically
            app.logger.error("Connection failed: %s", e)
            return jsonify({"error": "Server connection failed"}), 500
        except Timeout:
            # Handle timeout errors specifically
            app.logger.error("The request to the server timed out.")
            return jsonify({"error": "Server request timed out"}), 500
        except RequestException as e:
            # Handle other request-related errors
            app.logger.error("An unexpected request error occurred: %s", e)
            return (
                jsonify({"error": "Failed to add trailers due to a request error"}),
                500,
            )

    def add_trailer(item):
        """
        Helper function to add an individual trailer to the database.

        Parameters:
            item (dict): A single item from the YouTube API response containing trailer details.

        Returns:
            Response: A success status with the newly added movie or an error message.
        """
        title = item["snippet"]["title"]
        url = f"https://www.youtube.com/watch?v={item['id']['videoId']}"

        db.session.rollback()
        new_trailer = Trailer(url=url)
        db.session.add(new_trailer)

        db.session.commit()

        new_movie = Movie(title=title, url=url)

        try:
            db.session.add(new_movie)
            db.session.commit()
            return jsonify(message="The movies added successfully"), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            error_info = str(e.__dict__.get("orig", e))
            return jsonify(error=error_info), 400

    @app.route("/trigger_search", methods=["POST"])
    def trigger_search():
        """
        A route to trigger the search for movie trailers.

        Returns:
            Response: A success or error response.
        """
        # search_trailers()
        movie_list = [
            "The Witch",
            "Hereditary",
            "The Conjuring",
        ]  # Replace with your list of movies
        for movie in movie_list:
            search_trailers(movie)

        return jsonify({"message": "Search completed successfully"}), 200

    @app.route("/")
    def hello_world():
        """
        A simple route serving the home page with a greeting message.

        Returns:
            str: A welcome message.
        """
        return "Hello, World! This is the home page."

    @app.route("/api/movies", methods=["GET"])
    def get_movies():
        """
        A route to fetch and return all movies from the database.

        Returns:
            Response: A list of all movies or an error message.
        """
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
                    "url": movie.url,
                }
                for movie in movies
            ]
            return jsonify(movies_list), 200
        except SQLAlchemyError as e:
            app.logger.error(
                "Error fetching movies: %s", e
            )  # Using %s for lazy formatting
            return jsonify(error="An error occurred fetching movies"), 500

    return app


if __name__ == "__main__":
    flask_app = create_app()
    flask_app.run(host="localhost", port=8000)
