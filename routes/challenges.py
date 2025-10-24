"""Challenge routes"""
from flask import Blueprint, jsonify, render_template, redirect, url_for
import json
import glob
import random
import os

challenges_bp = Blueprint('challenges', __name__)


def load_all_challenges(language='python'):
    """Helper function to load all challenges from JSON files for a specific language"""
    challenges_data = []
    challenge_files = sorted(glob.glob(f'data/challenges/{language}/*.json'))
    
    for file_path in challenge_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                challenge = json.load(f)
                challenges_data.append(challenge)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
    
    return challenges_data


def load_challenge_by_number(problem_number, language='python'):
    """Helper function to load a specific challenge by problem number"""
    challenges = load_all_challenges(language)
    for challenge in challenges:
        if challenge.get('problem_number') == problem_number:
            return challenge
    return None


@challenges_bp.route('/api/challenges/by-language')
def get_challenges_by_language():
    """Get count of challenges for each programming language"""
    language_counts = {}
    
    # Get all language directories
    challenges_dir = 'data/challenges'
    if os.path.exists(challenges_dir):
        for item in os.listdir(challenges_dir):
            item_path = os.path.join(challenges_dir, item)
            if os.path.isdir(item_path):
                # Count JSON files in this language directory
                json_files = glob.glob(os.path.join(item_path, '*.json'))
                language_counts[item] = len(json_files)
    
    return jsonify(language_counts)


@challenges_bp.route('/get-challenges')
def get_challenges():
    """Get all available challenges - served from JSON files"""
    challenges_data = load_all_challenges()
    return jsonify(challenges_data)


@challenges_bp.route('/api/challenges/data')
def get_challenges_data():
    """API endpoint to get all challenges data for IndexedDB"""
    return get_challenges()


@challenges_bp.route('/api/challenges/by-difficulty')
def get_challenges_by_difficulty():
    """Get challenges filtered by programming language"""
    from flask import request
    language = request.args.get('language', 'python')
    
    # Load challenges for the specified language
    challenges = load_all_challenges(language)
    
    return jsonify({'challenges': challenges})


@challenges_bp.route('/difficulty-selector')
def difficulty_selector():
    """Display difficulty selector page"""
    return render_template('difficulty_selector.html')


@challenges_bp.route('/random-challenge/<difficulty>')
def random_challenge(difficulty):
    """Get a random challenge by difficulty level - returns JSON for AJAX (deprecated, use language-specific endpoint)"""
    from flask import request
    language = request.args.get('language', 'python')
    
    valid_difficulties = ['foundational', 'easy', 'average', 'difficult']
    
    if difficulty.lower() not in valid_difficulties:
        return jsonify({'error': 'Invalid difficulty level'}), 400
    
    # Load all challenges for the specified language
    challenges = load_all_challenges(language)
    
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


@challenges_bp.route('/api/random-challenge/<language>/<difficulty>')
def random_challenge_language(language, difficulty):
    """Get a random challenge by language and difficulty level - returns JSON for AJAX"""
    valid_difficulties = ['foundational', 'easy', 'average', 'difficult']
    
    if difficulty.lower() not in valid_difficulties:
        return jsonify({'error': 'Invalid difficulty level'}), 400
    
    # Load all challenges for the specified language
    challenges = load_all_challenges(language)
    
    # Filter by difficulty
    filtered_challenges = [
        c for c in challenges 
        if c.get('difficulty', '').lower() == difficulty.lower()
    ]
    
    if not filtered_challenges:
        return jsonify({'error': f'No challenges found for {language} with difficulty: {difficulty}'}), 404
    
    # Select a random challenge
    selected_challenge = random.choice(filtered_challenges)
    
    # Return JSON with the challenge details
    return jsonify({
        'problem_number': selected_challenge['problem_number'],
        'problem_name': selected_challenge['problem_name'],
        'difficulty': selected_challenge['difficulty'],
        'language': language
    })


@challenges_bp.route('/random/<difficulty>')
def random_challenge_direct(difficulty):
    """Directly navigate to a random challenge by difficulty - returns HTML (deprecated, use language-specific endpoint)"""
    from flask import request
    language = request.args.get('language', 'python')
    
    valid_difficulties = ['foundational', 'easy', 'average', 'difficult']
    
    if difficulty.lower() not in valid_difficulties:
        return render_template('404.html', message='Invalid difficulty level'), 404
    
    # Load all challenges for the specified language
    challenges = load_all_challenges(language)
    
    # Filter by difficulty
    filtered_challenges = [
        c for c in challenges 
        if c.get('difficulty', '').lower() == difficulty.lower()
    ]
    
    if not filtered_challenges:
        return render_template('404.html', message=f'No challenges found for difficulty: {difficulty}'), 404
    
    # Select a random challenge
    selected_challenge = random.choice(filtered_challenges)
    
    # Render the challenge page directly
    return render_template('challenge.html', challenge=selected_challenge)


@challenges_bp.route('/random/<language>/<difficulty>')
def random_challenge_language_direct(language, difficulty):
    """Directly navigate to a random challenge by language and difficulty - returns HTML"""
    valid_difficulties = ['foundational', 'easy', 'average', 'difficult']
    
    if difficulty.lower() not in valid_difficulties:
        return render_template('404.html', message='Invalid difficulty level'), 404
    
    # Load all challenges for the specified language
    challenges = load_all_challenges(language)
    
    # Filter by difficulty
    filtered_challenges = [
        c for c in challenges 
        if c.get('difficulty', '').lower() == difficulty.lower()
    ]
    
    if not filtered_challenges:
        return render_template('404.html', message=f'No {language} challenges found for difficulty: {difficulty}'), 404
    
    # Select a random challenge
    selected_challenge = random.choice(filtered_challenges)
    
    # Render the challenge page directly
    return render_template('challenge.html', challenge=selected_challenge)


@challenges_bp.route('/challenge/<int:problem_number>')
def view_challenge(problem_number):
    """Display a specific challenge"""
    challenge = load_challenge_by_number(problem_number)
    
    if not challenge:
        return render_template('404.html', message='Challenge not found'), 404
    
    return render_template('challenge.html', challenge=challenge)

