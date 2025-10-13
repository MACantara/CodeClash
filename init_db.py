"""
Helper script to create database tables and seed initial data
Run this after setting up your MySQL database
"""
from config import create_app, init_database

if __name__ == '__main__':
    print("Initializing CodeClash database...")
    app = create_app()
    
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Initialize database
    init_database(app)
    
    print("\nDatabase initialization complete!")
    print("You can now run the application with: python app.py")
