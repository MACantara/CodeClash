"""Match routes (create, view, submit, status)"""
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from models import db, Match
from utils import run_code_tests

matches_bp = Blueprint('matches', __name__)


@matches_bp.route('/match/create', methods=['POST'])
def create_match():
    """Create a new practice match"""
    data = request.json
    challenge_id = data.get('challenge_id')
    
    if not challenge_id:
        return jsonify({'success': False, 'message': 'Challenge is required'})
    
    try:
        match = Match(
            challenge_id=challenge_id,
            status='active',
            started_at=datetime.utcnow()
        )
        db.session.add(match)
        db.session.commit()
        
        return jsonify({'success': True, 'match_id': match.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@matches_bp.route('/match/<int:match_id>')
def match(match_id):
    """Match page"""
    match_obj = db.session.get(Match, match_id)
    
    if not match_obj:
        return "Match not found", 404
    
    # Start timer when first player enters (change from pending to active)
    if match_obj.status == 'pending':
        match_obj.status = 'active'
        match_obj.started_at = datetime.utcnow()
        db.session.commit()
    
    # Build match data dict for template
    match_data = {
        'id': match_obj.id,
        'challenge_id': match_obj.challenge_id,
        'status': match_obj.status,
        'player_code': match_obj.player_code,
        'player_errors': match_obj.player_errors,
        'player_time': match_obj.player_time,
        'player_submitted': match_obj.player_submitted,
        'started_at': match_obj.started_at.isoformat() + 'Z' if match_obj.started_at else None,
        'title': match_obj.challenge.title,
        'description': match_obj.challenge.description,
        'difficulty': match_obj.challenge.difficulty,
        'starter_code': match_obj.challenge.starter_code,
        'test_cases': match_obj.challenge.test_cases,
    }
    
    return render_template('match.html', match=match_data)


@matches_bp.route('/match/<int:match_id>/run', methods=['POST'])
def run_solution(match_id):
    """Run code without submitting (for testing)"""
    data = request.json
    code = data.get('code')
    
    match_obj = db.session.get(Match, match_id)
    
    if not match_obj:
        return jsonify({'success': False, 'message': 'Match not found'})
    
    # Run test cases
    test_cases = match_obj.challenge.get_test_cases()
    results = run_code_tests(code, test_cases)
    
    return jsonify({
        'success': True,
        'passed': results['passed'],
        'total': results['total'],
        'errors': results['errors'],
        'test_results': results['details']
    })


@matches_bp.route('/match/<int:match_id>/submit', methods=['POST'])
def submit_solution(match_id):
    """Submit solution for a match"""
    data = request.json
    code = data.get('code')
    
    match_obj = db.session.get(Match, match_id)
    
    if not match_obj:
        return jsonify({'success': False, 'message': 'Match not found'})
    
    # Run test cases
    test_cases = match_obj.challenge.get_test_cases()
    results = run_code_tests(code, test_cases)
    
    # Calculate completion time from when match started
    started_at = match_obj.started_at if match_obj.started_at else datetime.utcnow()
    completion_time = (datetime.utcnow() - started_at).total_seconds()
    
    # Update match data
    match_obj.player_code = code
    match_obj.player_errors = results['errors']
    match_obj.player_time = completion_time
    match_obj.player_submitted = True
    match_obj.status = 'completed'
    match_obj.ended_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'passed': results['passed'],
        'total': results['total'],
        'errors': results['errors'],
        'completion_time': completion_time,
        'test_results': results['details']
    })


@matches_bp.route('/match/<int:match_id>/status')
def match_status(match_id):
    """Get current match status"""
    match = db.session.get(Match, match_id)
    
    if not match:
        return jsonify({'success': False, 'message': 'Match not found'})
    
    match_data = {
        'id': match.id,
        'challenge_id': match.challenge_id,
        'player_submitted': match.player_submitted,
        'player_errors': match.player_errors,
        'player_time': match.player_time,
        'status': match.status,
        'created_at': match.created_at.isoformat() if match.created_at else None,
        'started_at': match.started_at.isoformat() if match.started_at else None,
        'ended_at': match.ended_at.isoformat() if match.ended_at else None,
    }
    
    return jsonify(match_data)
