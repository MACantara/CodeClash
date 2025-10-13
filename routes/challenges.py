"""Challenge routes"""
from flask import Blueprint, jsonify
from models import Challenge

challenges_bp = Blueprint('challenges', __name__)


@challenges_bp.route('/challenges')
def get_challenges():
    """Get all available challenges"""
    challenges = Challenge.query.order_by(Challenge.difficulty).all()
    
    challenges_data = []
    for c in challenges:
        challenges_data.append({
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'difficulty': c.difficulty,
            'starter_code': c.starter_code,
            'test_cases': c.test_cases,
            'time_limit': c.time_limit
        })
    
    return jsonify(challenges_data)
