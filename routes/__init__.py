"""
Routes package initialization.
Registers all blueprints with the Flask app.
"""
from flask import Flask


def register_blueprints(app: Flask):
    """Register all blueprints with the Flask app."""
    from .challenges import challenges_bp
    from .matches import matches_bp
    from .pages import pages_bp
    
    app.register_blueprint(challenges_bp)
    app.register_blueprint(matches_bp)
    app.register_blueprint(pages_bp)
