"""
Configuration and initialization for CodeClash with SQLAlchemy
"""
from flask import Flask
from models import db
from dotenv import load_dotenv
import os
import secrets

# Load environment variables
load_dotenv()

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Secret key for sessions
    app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))
    
    # Database configuration
    database_url = os.getenv('DATABASE_URL')
    
    # For local development, use SQLite if Railway MySQL is not accessible
    # For production on Railway, the internal hostname will work
    if database_url:
        # MySQL connection requires pymysql
        if database_url.startswith('mysql://'):
            database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)
        
        # Check if this is Railway internal hostname (only works in Railway environment)
        if 'railway.internal' in database_url:
            print("Note: Railway internal hostname detected.")
            print("This will only work when deployed on Railway.")
            print("For local development, using SQLite instead.\n")
            database_url = 'sqlite:///codeclash.db'
    else:
        database_url = 'sqlite:///codeclash.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }
    
    # Initialize SQLAlchemy
    db.init_app(app)
    
    return app

def init_database(app):
    """Initialize database tables"""
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Seed data
        from seed_data import seed_all
        seed_all()

if __name__ == '__main__':
    app = create_app()
    init_database(app)
