"""
Models package initialization.
Exports all models for easy importing.
"""
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# Import all models
from .user import User, UserStatistics
from .challenge import Challenge
from .match import Match
from .lobby import Lobby, LobbyPlayer, LobbyInvitation
from .chat import ChatMessage
from .achievement import Achievement, UserAchievement

# Export all models
__all__ = [
    'db',
    'User',
    'UserStatistics',
    'Challenge',
    'Match',
    'Lobby',
    'LobbyPlayer',
    'LobbyInvitation',
    'ChatMessage',
    'Achievement',
    'UserAchievement',
]
