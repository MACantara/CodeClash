"""Challenge data structure - No longer a database model
Data is now stored in IndexedDB on the client side
"""
from datetime import datetime
import json


class Challenge:
    """Challenge data structure for reference"""
    
    def __init__(self, id=None, title='', description='', difficulty='', 
                 starter_code='', test_cases=None, time_limit=300, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.difficulty = difficulty
        self.starter_code = starter_code
        self.test_cases = test_cases or []
        self.time_limit = time_limit
        self.created_at = created_at or datetime.utcnow()
    
    def get_test_cases(self):
        """Get test cases as list"""
        if isinstance(self.test_cases, str):
            return json.loads(self.test_cases)
        return self.test_cases
    
    def set_test_cases(self, test_cases_list):
        """Set test cases from list"""
        self.test_cases = json.dumps(test_cases_list) if isinstance(test_cases_list, list) else test_cases_list
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'starter_code': self.starter_code,
            'test_cases': self.get_test_cases(),
            'time_limit': self.time_limit,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else str(self.created_at)
        }
    
    def __repr__(self):
        return f'<Challenge {self.title}>'

