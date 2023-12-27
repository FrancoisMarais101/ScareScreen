"""
models/database.py
------------------

This module defines the database models using SQLAlchemy for an application. 
It includes classes representing entities like movies, trailers, users, and other related entities in a 
media application context. 
Each class corresponds to a table in the database with the specified columns and relationships.

Classes:
    Movie: Represents movies with attributes like title, director, and cast.
    Trailer: Represents movie trailers with attributes like URL, duration, and associated movie.
    StreamingPlatform: Represents streaming platforms with attributes like name and URL.
    PlatformTrailer: Represents the association between trailers and platforms.
    User: Represents users with attributes like username, email, and password.
    Review: Represents reviews with attributes like rating and review text.
    Recommendation: Represents recommendations with attributes like score.
    Notification: Represents notifications with attributes like type and message.
    Watchlist: Represents a user's watchlist with attributes like date added.
"""
from extensions import db


# pylint: disable=too-few-public-methods
class Movie(db.Model):
    """
    A class representing the 'movies' table in the database.

    Attributes:
        id: Primary key.
        title: Title of the movie.
        director: Director of the movie.
        cast: Cast of the movie.
        release_date: Release date of the movie.
        length: Length of the movie in minutes.
        rating: Average rating of the movie.
        age_restriction: Age restriction for the movie.
        summary: Brief summary of the movie.
        trailers: Relationship to associated trailers.
    """

    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    director = db.Column(db.String(100))
    cast = db.Column(db.String(500))
    release_date = db.Column(db.Date)
    length = db.Column(db.Integer)  # length in minutes
    rating = db.Column(db.Float)  # average rating
    age_restriction = db.Column(db.Integer)
    summary = db.Column(db.String(1000))

    trailers = db.relationship("Trailer", back_populates="movie")


# pylint: disable=too-few-public-methods
class Trailer(db.Model):
    """
    A class representing the 'trailers' table in the database.

    Attributes:
        id: Primary key.
        movie_id: ForeignKey to the associated movie.
        url: URL of the trailer.
        duration: Duration of the trailer in seconds.
        release_date: Release date of the trailer.
        description: Description of the trailer.
        movie: Relationship to the associated movie.
        platform_trailers: Relationship to the associated platforms.
    """

    __tablename__ = "trailers"

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))
    url = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.Integer)  # duration in seconds
    release_date = db.Column(db.Date)
    description = db.Column(db.String(500))

    movie = db.relationship("Movie", back_populates="trailers")
    platform_trailers = db.relationship("PlatformTrailer", back_populates="trailer")


# pylint: disable=too-few-public-methods
class StreamingPlatform(db.Model):
    """
    Represents streaming platforms, detailing the platform name and URL.

    Attributes:
        id: Primary key.
        name: Name of the streaming platform.
        url: URL of the streaming platform.
        platform_trailers: Relationship to trailers available on the platform.
    """

    __tablename__ = "streaming_platforms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500))

    platform_trailers = db.relationship("PlatformTrailer", back_populates="platform")


# pylint: disable=too-few-public-methods
class PlatformTrailer(db.Model):
    """
    Represents the association between trailers and the platforms they are available on.

    Attributes:
        id: Primary key.
        trailer_id: ForeignKey to the associated trailer.
        platform_id: ForeignKey to the associated streaming platform.
        trailer: Relationship to the trailer entity.
        platform: Relationship to the streaming platform entity.
    """

    __tablename__ = "platform_trailers"

    id = db.Column(db.Integer, primary_key=True)
    trailer_id = db.Column(db.Integer, db.ForeignKey("trailers.id"))
    platform_id = db.Column(db.Integer, db.ForeignKey("streaming_platforms.id"))

    trailer = db.relationship("Trailer", back_populates="platform_trailers")
    platform = db.relationship("StreamingPlatform", back_populates="platform_trailers")


# pylint: disable=too-few-public-methods
class User(db.Model):
    """
    Represents users, including their credentials and personal information.

    Attributes:
        id: Primary key.
        username: Unique username for the user.
        email: Unique email address for the user.
        password_hash: Hashed password for security.
        reviews: Relationship to reviews made by the user.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(
        db.String(128), nullable=False
    )  # Always store hashed passwords

    reviews = db.relationship("Review", back_populates="user")


# pylint: disable=too-few-public-methods
class Review(db.Model):
    """
    Represents reviews for trailers, including ratings and text.

    Attributes:
        id: Primary key.
        user_id: ForeignKey to the user who made the review.
        trailer_id: ForeignKey to the trailer being reviewed.
        rating: Numeric rating given in the review.
        review_text: Text content of the review.
        user: Relationship to the user who made the review.
        trailer: Relationship to the trailer being reviewed.
    """

    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    trailer_id = db.Column(db.Integer, db.ForeignKey("trailers.id"))
    rating = db.Column(db.Float)
    review_text = db.Column(db.String(1000))

    user = db.relationship("User", back_populates="reviews")
    trailer = db.relationship("Trailer")


# pylint: disable=too-few-public-methods
class Recommendation(db.Model):
    """
    Represents recommendations of movies to users.

    Attributes:
        id: Primary key.
        user_id: ForeignKey to the user who received the recommendation.
        movie_id: ForeignKey to the recommended movie.
        score: Numeric score or weight of the recommendation.
        user: Relationship to the user.
        movie: Relationship to the movie.
    """

    __tablename__ = "recommendations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))
    score = db.Column(db.Float)

    user = db.relationship("User")
    movie = db.relationship("Movie")


# pylint: disable=too-few-public-methods
class Notification(db.Model):
    """
    Represents notifications sent to users.

    Attributes:
        id: Primary key.
        user_id: ForeignKey to the user who received the notification.
        type: Type or category of the notification.
        message: Content of the notification.
        user: Relationship to the user.
    """

    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    type = db.Column(db.String(100))
    message = db.Column(db.String(500))

    user = db.relationship("User")


# pylint: disable=too-few-public-methods
class Watchlist(db.Model):
    """
    Represents users' watchlists, detailing movies added for future viewing.

    Attributes:
        id: Primary key.
        user_id: ForeignKey to the user who owns the watchlist.
        movie_id: ForeignKey to the movie added to the watchlist.
        date_added: Date when the movie was added to the watchlist.
        user: Relationship to the user.
        movie: Relationship to the movie.
    """

    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))
    date_added = db.Column(db.Date)

    user = db.relationship("User")
    movie = db.relationship("Movie")
