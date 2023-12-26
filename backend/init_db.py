# init_db.py
from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    print("Creating database tables...")

    # Now creates tables for all imported models
    db.create_all()
    print("Tables created successfully")
