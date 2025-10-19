"""
Routes package initialization.
Registers all blueprints with the Flask app.
"""
from flask import Flask


def register_blueprints(app: Flask):
    """Register all blueprints with the Flask app."""
    from .auth import auth_bp
    from .challenges import challenges_bp
    from .matches import matches_bp
    from .lobby import lobby_bp
    from .profile import profile_bp
    from .chat import chat_bp
    from .pages import pages_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(challenges_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(lobby_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(pages_bp)
