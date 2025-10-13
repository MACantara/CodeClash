"""
Helper script to create database tables and seed initial data
Run this after setting up your MySQL database

⚠️  WARNING: This script will DROP all existing tables and recreate them!
All data will be lost!
"""
from config import create_app, init_database
from models import db

if __name__ == '__main__':
    print("=" * 70)
    print("⚠️  WARNING: DATABASE RESET SCRIPT")
    print("=" * 70)
    print("This script will:")
    print("  1. DROP all existing tables")
    print("  2. CREATE new tables")
    print("  3. SEED initial data (challenges and achievements)")
    print("\n❌ ALL EXISTING DATA WILL BE LOST!")
    print("=" * 70)
    
    # Ask for confirmation
    response = input("\nDo you want to continue? Type 'YES' to proceed: ")
    
    if response != 'YES':
        print("\n❌ Operation cancelled. No changes were made.")
        exit(0)
    
    print("\n🔄 Initializing CodeClash database...")
    app = create_app()
    
    print(f"📊 Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # Drop all existing tables
    print("\n🗑️  Dropping existing tables...")
    with app.app_context():
        db.drop_all()
        print("✅ All tables dropped successfully!")
    
    # Initialize database (create tables and seed data)
    print("\n🔨 Creating new tables and seeding data...")
    init_database(app)
    
    print("\n" + "=" * 70)
    print("✅ Database initialization complete!")
    print("=" * 70)
    print("You can now run the application with: python app.py")
    print("=" * 70)
