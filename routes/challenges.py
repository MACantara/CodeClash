"""Challenge routes"""
from flask import Blueprint, jsonify, render_template, redirect, url_for
import json
import glob
import random

challenges_bp = Blueprint('challenges', __name__)


def load_all_challenges():
    """Helper function to load all challenges from JSON files"""
    challenges_data = []
    challenge_files = sorted(glob.glob('data/challenges/*.json'))
    
    for file_path in challenge_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                challenge = json.load(f)
                challenges_data.append(challenge)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return challenges_data


def load_challenge_by_number(problem_number):
    """Helper function to load a specific challenge by problem number"""
    challenges = load_all_challenges()
    for challenge in challenges:
        if challenge.get('problem_number') == problem_number:
            return challenge
    return None


@challenges_bp.route('/get-challenges')
def get_challenges():
    """Get all available challenges - served from JSON files"""
    challenges_data = load_all_challenges()
    return jsonify(challenges_data)


@challenges_bp.route('/api/challenges/data')
def get_challenges_data():
    """API endpoint to get all challenges data for IndexedDB"""
    return get_challenges()


@challenges_bp.route('/difficulty-selector')
def difficulty_selector():
    """Display difficulty selector page"""
    return render_template('difficulty_selector.html')


@challenges_bp.route('/random-challenge/<difficulty>')
def random_challenge(difficulty):
    """Get a random challenge by difficulty level - returns JSON"""
    valid_difficulties = ['foundational', 'easy', 'average', 'difficult']
    
    if difficulty.lower() not in valid_difficulties:
        return jsonify({'error': 'Invalid difficulty level'}), 400
    
    # Load all challenges
    challenges = load_all_challenges()
    
    # Filter by difficulty
    filtered_challenges = [
        c for c in challenges 
        if c.get('difficulty', '').lower() == difficulty.lower()
    ]
    
    if not filtered_challenges:
        return jsonify({'error': f'No challenges found for difficulty: {difficulty}'}), 404
    
    # Select a random challenge
    selected_challenge = random.choice(filtered_challenges)
    
    # Return JSON with the challenge details
    return jsonify({
        'problem_number': selected_challenge['problem_number'],
        'problem_name': selected_challenge['problem_name'],
        'difficulty': selected_challenge['difficulty']
    })


@challenges_bp.route('/challenge/<int:problem_number>')
def view_challenge(problem_number):
    """Display a specific challenge"""
    challenge = load_challenge_by_number(problem_number)
    
    if not challenge:
        return render_template('404.html', message='Challenge not found'), 404
    
    return render_template('challenge.html', challenge=challenge)


@challenges_bp.route('/api/run-code', methods=['POST'])
def run_code():
    """API endpoint to run/test code (placeholder for now)"""
    from flask import request
    
    data = request.get_json()
    code = data.get('code', '')
    problem_number = data.get('problem_number')
    test_mode = data.get('test_mode', False)
    
    # Load the challenge to get test cases
    challenge = load_challenge_by_number(problem_number)
    
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    
    # This is a placeholder - in a real implementation, you'd:
    # 1. Execute the code safely in a sandboxed environment
    # 2. Run it against the test cases
    # 3. Return the results
    
    # For now, return a mock response
    return jsonify({
        'error': 'Code execution is not yet implemented. This feature requires a secure sandbox environment.',
        'note': 'You can copy the code and test it locally in your Python environment.'
    })

