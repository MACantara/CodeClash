"""Challenge routes"""
from flask import Blueprint, jsonify
import json
import glob

challenges_bp = Blueprint('challenges', __name__)


@challenges_bp.route('/challenges')
def get_challenges():
    """Get all available challenges - served from JSON files"""
    challenges_data = []
    
    # Load challenges from JSON files
    challenge_files = sorted(glob.glob('data/challenges/*.json'))
    
    for file_path in challenge_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                challenge = json.load(f)
                challenges_data.append(challenge)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return jsonify(challenges_data)


@challenges_bp.route('/api/challenges/data')
def get_challenges_data():
    """API endpoint to get all challenges data for IndexedDB"""
    return get_challenges()

