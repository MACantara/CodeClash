"""Lobby, LobbyPlayer, and LobbyInvitation models"""
from datetime import datetime
from . import db


class Lobby(db.Model):
    __tablename__ = 'lobbies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    host_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    challenge_id = db.Column(db.Integer, db.ForeignKey('challenges.id'), nullable=False)
    max_players = db.Column(db.Integer, default=2)
    current_players = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='waiting')
    is_public = db.Column(db.Boolean, default=True)
    match_id = db.Column(db.Integer, db.ForeignKey('matches.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    host = db.relationship('User', foreign_keys=[host_id])
    challenge = db.relationship('Challenge')
    match = db.relationship('Match', foreign_keys=[match_id])
    players = db.relationship('LobbyPlayer', backref='lobby', cascade='all, delete-orphan')
    invitations = db.relationship('LobbyInvitation', backref='lobby', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Lobby {self.name}>'


class LobbyPlayer(db.Model):
    __tablename__ = 'lobby_players'
    
    id = db.Column(db.Integer, primary_key=True)
    lobby_id = db.Column(db.Integer, db.ForeignKey('lobbies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ready = db.Column(db.Boolean, default=False)
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<LobbyPlayer user_id={self.user_id} lobby_id={self.lobby_id}>'


class LobbyInvitation(db.Model):
    __tablename__ = 'lobby_invitations'
    
    id = db.Column(db.Integer, primary_key=True)
    lobby_id = db.Column(db.Integer, db.ForeignKey('lobbies.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id])
    receiver = db.relationship('User', foreign_keys=[receiver_id])
    
    def __repr__(self):
        return f'<LobbyInvitation {self.id}>'
