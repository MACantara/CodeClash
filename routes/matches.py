"""Match routes (create, view, submit, status)"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
from models import db, User, Match, UserStatistics
from utils import run_code_tests, determine_winner, check_and_award_achievements

matches_bp = Blueprint('matches', __name__)


@matches_bp.route('/match/create', methods=['POST'])
def create_match():
    """Create a new match"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    mode = data.get('mode', 'pvp')  # 'pvp' or 'practice'
    opponent_username = data.get('opponent')
    challenge_id = data.get('challenge_id')
    
    if mode == 'practice':
        # Practice mode - solo player
        try:
            match = Match(
                mode='practice',
                player1_id=session['user_id'],
                player2_id=None,
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
    else:
        # PvP mode - two players
        opponent = User.query.filter_by(username=opponent_username).first()
        
        if not opponent:
            return jsonify({'success': False, 'message': 'Opponent not found'})
        
        if opponent.id == session['user_id']:
            return jsonify({'success': False, 'message': 'Cannot play against yourself'})
        
        try:
            match = Match(
                mode='pvp',
                player1_id=session['user_id'],
                player2_id=opponent.id,
                challenge_id=challenge_id,
                status='pending'
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
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
    
    match_obj = db.session.get(Match, match_id)
    
    if not match_obj:
        return "Match not found", 404
    
    # For PvP: check if user is one of the players
    # For Practice: check if user is the player
    if match_obj.mode == 'practice':
        if session['user_id'] != match_obj.player1_id:
            return "Unauthorized", 403
    else:
        if session['user_id'] not in [match_obj.player1_id, match_obj.player2_id]:
            return "Unauthorized", 403
    
    # Start timer when first player enters (change from pending to active)
    if match_obj.status == 'pending':
        match_obj.status = 'active'
        match_obj.started_at = datetime.utcnow()
        db.session.commit()
    
    # Build match data dict for template
    match_data = {
        'id': match_obj.id,
        'mode': match_obj.mode,
        'player1_id': match_obj.player1_id,
        'player2_id': match_obj.player2_id,
        'challenge_id': match_obj.challenge_id,
        'status': match_obj.status,
        'player1_code': match_obj.player1_code,
        'player2_code': match_obj.player2_code,
        'player1_errors': match_obj.player1_errors,
        'player2_errors': match_obj.player2_errors,
        'player1_time': match_obj.player1_time,
        'player2_time': match_obj.player2_time,
        'player1_submitted': match_obj.player1_submitted,
        'player2_submitted': match_obj.player2_submitted,
        'started_at': match_obj.started_at.isoformat() + 'Z' if match_obj.started_at else None,
        'title': match_obj.challenge.title,
        'description': match_obj.challenge.description,
        'difficulty': match_obj.challenge.difficulty,
        'starter_code': match_obj.challenge.starter_code,
        'test_cases': match_obj.challenge.test_cases,
        'player1_name': match_obj.player1.username,
        'player2_name': match_obj.player2.username if match_obj.player2 else None
    }
    
    return render_template('match.html', match=match_data, user_id=session['user_id'])


@matches_bp.route('/match/<int:match_id>/run', methods=['POST'])
def run_solution(match_id):
    """Run code without submitting (for testing)"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    code = data.get('code')
    
    match_obj = db.session.get(Match, match_id)
    
    if not match_obj:
        return jsonify({'success': False, 'message': 'Match not found'})
    
    if session['user_id'] not in [match_obj.player1_id, match_obj.player2_id]:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
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
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    code = data.get('code')
    
    match_obj = db.session.get(Match, match_id)
    
    if not match_obj:
        return jsonify({'success': False, 'message': 'Match not found'})
    
    # Check authorization
    if match_obj.mode == 'practice':
        if session['user_id'] != match_obj.player1_id:
            return jsonify({'success': False, 'message': 'Unauthorized'})
    else:
        if session['user_id'] not in [match_obj.player1_id, match_obj.player2_id]:
            return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Run test cases
    test_cases = match_obj.challenge.get_test_cases()
    results = run_code_tests(code, test_cases)
    
    # Calculate completion time from when match started
    started_at = match_obj.started_at if match_obj.started_at else datetime.utcnow()
    completion_time = (datetime.utcnow() - started_at).total_seconds()
    
    # Determine which player submitted and update
    if session['user_id'] == match_obj.player1_id:
        match_obj.player1_code = code
        match_obj.player1_errors = results['errors']
        match_obj.player1_time = completion_time
        match_obj.player1_submitted = True
    else:
        match_obj.player2_code = code
        match_obj.player2_errors = results['errors']
        match_obj.player2_time = completion_time
        match_obj.player2_submitted = True
    
    db.session.commit()
    
    # Handle completion based on mode
    if match_obj.mode == 'practice':
        # Practice mode: mark as complete after submission
        match_obj.status = 'completed'
        match_obj.ended_at = datetime.utcnow()
        
        # Update practice player statistics
        player = db.session.get(User, match_obj.player1_id)
        player.total_matches += 1
        
        player_stats = player.statistics
        if not player_stats:
            player_stats = UserStatistics(user_id=match_obj.player1_id)
            db.session.add(player_stats)
            db.session.flush()
        
        # Update fastest time
        fastest_time = player_stats.fastest_solve_time
        if fastest_time is None or completion_time < fastest_time:
            fastest_time = completion_time
        
        # Update average time
        avg_time = player_stats.average_solve_time or 0
        new_avg = ((avg_time * (player.total_matches - 1)) + completion_time) / player.total_matches if player.total_matches > 0 else completion_time
        
        player_stats.fastest_solve_time = fastest_time
        player_stats.average_solve_time = new_avg
        player_stats.challenges_solved += 1
        
        # Check for perfect practice
        if results['errors'] == 0:
            player_stats.perfect_matches += 1
        
        check_and_award_achievements(match_obj.player1_id)
        
    else:
        # PvP mode: check if both players have submitted
        if match_obj.player1_submitted and match_obj.player2_submitted:
            # Determine winner
            winner_id = determine_winner(match_obj)
            loser_id = match_obj.player1_id if winner_id == match_obj.player2_id else match_obj.player2_id
            
            # Update match status
            match_obj.status = 'completed'
            match_obj.ended_at = datetime.utcnow()
            match_obj.winner_id = winner_id
            
            # Update user basic stats
            winner = db.session.get(User, winner_id)
            loser = db.session.get(User, loser_id)
            winner.wins += 1
            winner.total_matches += 1
            winner.rating += 25
            loser.losses += 1
            loser.total_matches += 1
            loser.rating -= 10
            
            # Update detailed statistics for winner
            winner_errors = match_obj.player1_errors if winner_id == match_obj.player1_id else match_obj.player2_errors
            winner_time = match_obj.player1_time if winner_id == match_obj.player1_id else match_obj.player2_time
            
            # Check if perfect match
            is_perfect = winner_errors == 0
            
            # Get or create stats
            winner_stats = winner.statistics
            if not winner_stats:
                winner_stats = UserStatistics(user_id=winner_id)
                db.session.add(winner_stats)
                db.session.flush()
            
            # Update win streak
            new_streak = winner_stats.current_win_streak + 1
            best_streak = max(new_streak, winner_stats.best_win_streak)
            
            # Update fastest time
            fastest_time = winner_stats.fastest_solve_time
            if fastest_time is None or winner_time < fastest_time:
                fastest_time = winner_time
            
            # Update average time
            avg_time = winner_stats.average_solve_time or 0
            new_avg = ((avg_time * (winner.wins - 1)) + winner_time) / winner.wins if winner.wins > 0 else winner_time
            
            # Update winner statistics
            winner_stats.current_win_streak = new_streak
            winner_stats.best_win_streak = best_streak
            winner_stats.fastest_solve_time = fastest_time
            winner_stats.average_solve_time = new_avg
            winner_stats.challenges_solved += 1
            if is_perfect:
                winner_stats.perfect_matches += 1
            
            # Reset loser's win streak
            loser_stats = loser.statistics
            if loser_stats:
                loser_stats.current_win_streak = 0
            
            # Check and award achievements
            check_and_award_achievements(winner_id)
            check_and_award_achievements(loser_id)
    
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
    
    if match.mode == 'practice':
        # Practice mode status
        match_data = {
            'id': match.id,
            'mode': 'practice',
            'player1_id': match.player1_id,
            'player2_id': None,
            'player1_name': match.player1.username,
            'player2_name': None,
            'player1_submitted': match.player1_submitted,
            'player2_submitted': True,  # No opponent in practice
            'player1_errors': match.player1_errors,
            'player2_errors': 0,
            'player1_time': match.player1_time,
            'player2_time': 0,
            'status': match.status,
            'created_at': match.created_at.isoformat() if match.created_at else None,
            'started_at': match.started_at.isoformat() if match.started_at else None,
            'ended_at': match.ended_at.isoformat() if match.ended_at else None,
            'winner_id': match.player1_id if match.status == 'completed' else None,
            'winner_name': match.player1.username if match.status == 'completed' else None
        }
    else:
        # PvP mode status
        match_data = {
            'id': match.id,
            'mode': 'pvp',
            'player1_id': match.player1_id,
            'player2_id': match.player2_id,
            'player1_name': match.player1.username,
            'player2_name': match.player2.username,
            'player1_submitted': match.player1_submitted,
            'player2_submitted': match.player2_submitted,
            'player1_errors': match.player1_errors,
            'player2_errors': match.player2_errors,
            'player1_time': match.player1_time,
            'player2_time': match.player2_time,
            'status': match.status,
            'created_at': match.created_at.isoformat() if match.created_at else None,
            'started_at': match.started_at.isoformat() if match.started_at else None,
            'ended_at': match.ended_at.isoformat() if match.ended_at else None,
            'winner_id': match.winner_id,
            'winner_name': match.winner.username if match.winner else None
        }
    
    return jsonify(match_data)
