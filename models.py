from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    total_matches = db.Column(db.Integer, default=0)
    rating = db.Column(db.Integer, default=1000)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    statistics = db.relationship('UserStatistics', backref='user', uselist=False, cascade='all, delete-orphan')
    achievements = db.relationship('UserAchievement', backref='user', cascade='all, delete-orphan')
    friendships_sent = db.relationship('Friendship', foreign_keys='Friendship.user_id', backref='sender', cascade='all, delete-orphan')
    friendships_received = db.relationship('Friendship', foreign_keys='Friendship.friend_id', backref='receiver', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'

class Challenge(db.Model):
    __tablename__ = 'challenges'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    starter_code = db.Column(db.Text)
    test_cases = db.Column(db.Text, nullable=False)  # JSON string
    time_limit = db.Column(db.Integer, default=300)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_test_cases(self):
        return json.loads(self.test_cases)
    
    def set_test_cases(self, test_cases_list):
        self.test_cases = json.dumps(test_cases_list)
    
    def __repr__(self):
        return f'<Challenge {self.title}>'

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
    messages = db.relationship('ChatMessage', backref='lobby', cascade='all, delete-orphan')
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

class Friendship(db.Model):
    __tablename__ = 'friendships'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Friendship {self.user_id}->{self.friend_id} ({self.status})>'

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

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    lobby_id = db.Column(db.Integer, db.ForeignKey('lobbies.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<ChatMessage {self.id}>'

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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User')
    
    def __repr__(self):
        return f'<CodeSnapshot match_id={self.match_id} user_id={self.user_id}>'

class Achievement(db.Model):
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='bi-trophy-fill')
    points = db.Column(db.Integer, default=10)
    criteria = db.Column(db.Text, nullable=False)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_criteria(self):
        return json.loads(self.criteria)
    
    def set_criteria(self, criteria_dict):
        self.criteria = json.dumps(criteria_dict)
    
    def __repr__(self):
        return f'<Achievement {self.name}>'

class UserAchievement(db.Model):
    __tablename__ = 'user_achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievements.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    achievement = db.relationship('Achievement')
    
    def __repr__(self):
        return f'<UserAchievement user_id={self.user_id} achievement_id={self.achievement_id}>'

class UserStatistics(db.Model):
    __tablename__ = 'user_statistics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    current_win_streak = db.Column(db.Integer, default=0)
    best_win_streak = db.Column(db.Integer, default=0)
    fastest_solve_time = db.Column(db.Float)
    average_solve_time = db.Column(db.Float)
    total_solve_time = db.Column(db.Float, default=0)
    challenges_solved = db.Column(db.Integer, default=0)
    perfect_matches = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserStatistics user_id={self.user_id}>'
