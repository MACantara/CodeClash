"""Match data structure - No longer a database model
Data is now stored in IndexedDB on the client side
"""
from datetime import datetime


class Match:
    """Match data structure for reference"""
    
    def __init__(self, id=None, challenge_id=None, status='active', 
                 player_code='', player_errors=0, player_time=0, 
                 player_submitted=False, player_completed=False,
                 started_at=None, ended_at=None, created_at=None):
        self.id = id
        self.challenge_id = challenge_id
        self.status = status
        self.player_code = player_code
        self.player_errors = player_errors
        self.player_time = player_time
        self.player_submitted = player_submitted
        self.player_completed = player_completed
        self.started_at = started_at
        self.ended_at = ended_at
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'challenge_id': self.challenge_id,
            'status': self.status,
            'player_code': self.player_code,
            'player_errors': self.player_errors,
            'player_time': self.player_time,
            'player_submitted': self.player_submitted,
            'player_completed': self.player_completed,
            'started_at': self.started_at.isoformat() if hasattr(self.started_at, 'isoformat') else str(self.started_at) if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if hasattr(self.ended_at, 'isoformat') else str(self.ended_at) if self.ended_at else None,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else str(self.created_at)
        }
    
    def __repr__(self):
        return f'<Match {self.id}>'

