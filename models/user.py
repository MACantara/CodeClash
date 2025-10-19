"""User and UserStatistics models"""
from datetime import datetime
from . import db


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
    
    def __repr__(self):
        return f'<User {self.username}>'


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
