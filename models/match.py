"""Match model"""
from datetime import datetime
from . import db


class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    status = db.Column(db.String(20), default='active')
    player_code = db.Column(db.Text)
    player_errors = db.Column(db.Integer, default=0)
    player_time = db.Column(db.Float, default=0)
    player_submitted = db.Column(db.Boolean, default=False)
    player_completed = db.Column(db.Boolean, default=False)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    challenge = db.relationship('Challenge')
    
    def __repr__(self):
        return f'<Match {self.id}>'
