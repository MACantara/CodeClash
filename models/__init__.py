"""
Models package initialization.
Exports all models for easy importing.
"""
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Import all models
from .challenge import Challenge
from .match import Match

# Export all models
__all__ = [
    'db',
    'Challenge',
    'Match',
]
