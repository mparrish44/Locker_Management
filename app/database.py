# app/database.py
from app.extensions import db

def init_db(app):
    """
    Initialize the database with the given Flask app.
    """
    db.init_app(app)