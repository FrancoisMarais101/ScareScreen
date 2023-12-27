"""
init_db.py
------

A Python script to create the database tables.

"""
from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    print("Creating database tables...")

    # Now creates tables for all imported models
    db.create_all()
    print("Tables created successfully")
