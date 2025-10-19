"""Match model"""
from datetime import datetime
from . import db


class Match(db.Model):
    __tablename__ = 'matches'
    
    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    player1_code = db.Column(db.Text)
    player2_code = db.Column(db.Text)
    player1_errors = db.Column(db.Integer, default=0)
    player2_errors = db.Column(db.Integer, default=0)
    player1_time = db.Column(db.Float, default=0)
    player2_time = db.Column(db.Float, default=0)
    player1_submitted = db.Column(db.Boolean, default=False)
    player2_submitted = db.Column(db.Boolean, default=False)
    player1_completed = db.Column(db.Boolean, default=False)
    player2_completed = db.Column(db.Boolean, default=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    player1 = db.relationship('User', foreign_keys=[player1_id])
    player2 = db.relationship('User', foreign_keys=[player2_id])
    challenge = db.relationship('Challenge')
    winner = db.relationship('User', foreign_keys=[winner_id])
    
    def __repr__(self):
        return f'<Match {self.id}>'
