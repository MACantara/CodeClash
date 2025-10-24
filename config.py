"""
Configuration for CodeClash - No database backend
Using IndexedDB for client-side storage
"""
from flask import Flask
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
    
    # No database configuration needed - using IndexedDB client-side
    print("✅ CodeClash configured with client-side IndexedDB storage")
    
    return app

