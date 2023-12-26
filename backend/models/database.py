# models/database.py
from extensions import db


class Movie(db.Model):
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


class Trailer(db.Model):
    __tablename__ = "trailers"

    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))
    url = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.Integer)  # duration in seconds
    release_date = db.Column(db.Date)
    description = db.Column(db.String(500))

    movie = db.relationship("Movie", back_populates="trailers")
    platform_trailers = db.relationship("PlatformTrailer", back_populates="trailer")


class StreamingPlatform(db.Model):
    __tablename__ = "streaming_platforms"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500))

    platform_trailers = db.relationship("PlatformTrailer", back_populates="platform")


class PlatformTrailer(db.Model):
    __tablename__ = "platform_trailers"

    id = db.Column(db.Integer, primary_key=True)
    trailer_id = db.Column(db.Integer, db.ForeignKey("trailers.id"))
    platform_id = db.Column(db.Integer, db.ForeignKey("streaming_platforms.id"))

    trailer = db.relationship("Trailer", back_populates="platform_trailers")
    platform = db.relationship("StreamingPlatform", back_populates="platform_trailers")


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(
        db.String(128), nullable=False
    )  # Always store hashed passwords

    reviews = db.relationship("Review", back_populates="user")


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    trailer_id = db.Column(db.Integer, db.ForeignKey("trailers.id"))
    rating = db.Column(db.Float)
    review_text = db.Column(db.String(1000))

    user = db.relationship("User", back_populates="reviews")
    trailer = db.relationship("Trailer")


class Recommendation(db.Model):
    __tablename__ = "recommendations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))
    score = db.Column(db.Float)

    user = db.relationship("User")
    movie = db.relationship("Movie")


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    type = db.Column(db.String(100))
    message = db.Column(db.String(500))

    user = db.relationship("User")


class Watchlist(db.Model):
    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))
    date_added = db.Column(db.Date)

    user = db.relationship("User")
    movie = db.relationship("Movie")
