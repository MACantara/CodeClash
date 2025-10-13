"""Challenge model"""
from datetime import datetime
import json
from . import db


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
