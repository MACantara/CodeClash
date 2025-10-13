"""Match, MatchSpectator, and CodeSnapshot models"""
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
    spectators = db.relationship('MatchSpectator', backref='match', cascade='all, delete-orphan')
    code_snapshots = db.relationship('CodeSnapshot', backref='match', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Match {self.id}>'


class MatchSpectator(db.Model):
    __tablename__ = 'match_spectators'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<MatchSpectator match_id={self.match_id} user_id={self.user_id}>'


class CodeSnapshot(db.Model):
    __tablename__ = 'code_snapshots'
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    code = db.Column(db.Text, nullable=False)
    elapsed_seconds = db.Column(db.Integer)  # Time elapsed since match start
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<CodeSnapshot match_id={self.match_id} user_id={self.user_id}>'
