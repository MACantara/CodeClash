"""Spectator routes (spectate, get data, list active matches)"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import db, Match, MatchSpectator

spectator_bp = Blueprint('spectator', __name__)


@spectator_bp.route('/match/<int:match_id>/spectate')
def spectate_match(match_id):
    """Spectate an ongoing match"""
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
    
    match = Match.query.filter(
        Match.id == match_id,
        Match.status.in_(['active', 'completed'])
    ).first()
    
    if not match:
        return "Match not found or not started", 404
    
    # Add as spectator
    existing = MatchSpectator.query.filter_by(
        match_id=match_id,
        user_id=session['user_id']
    ).first()
    
    if not existing:
        spectator = MatchSpectator(
            match_id=match_id,
            user_id=session['user_id']
        )
        db.session.add(spectator)
        db.session.commit()
    
    match_data = {
        'id': match.id,
        'challenge_name': match.challenge.title,
        'challenge_description': match.challenge.description,
        'difficulty': match.challenge.difficulty,
        'player1_name': match.player1.username,
        'player2_name': match.player2.username,
        'status': match.status,
        'player1_submitted': match.player1_submitted,
        'player2_submitted': match.player2_submitted
    }
    
    return render_template('spectate.html', match=match_data)


@spectator_bp.route('/match/<int:match_id>/spectator_data')
def get_spectator_data(match_id):
    """Get match data for spectators"""
    match = db.session.get(Match, match_id)
    
    if not match:
        return jsonify({'success': False, 'message': 'Match not found'})
    
    # Get spectator count
    spectator_count = MatchSpectator.query.filter_by(match_id=match_id).count()
    
    match_data = {
        'id': match.id,
        'player1_id': match.player1_id,
        'player2_id': match.player2_id,
        'player1_name': match.player1.username,
        'player2_name': match.player2.username,
        'challenge_id': match.challenge_id,
        'challenge_name': match.challenge.title,
        'challenge_description': match.challenge.description,
        'difficulty': match.challenge.difficulty,
        'status': match.status,
        'player1_submitted': match.player1_submitted,
        'player2_submitted': match.player2_submitted,
        'player1_errors': match.player1_errors,
        'player2_errors': match.player2_errors,
        'started_at': match.started_at.isoformat() if match.started_at else None,
        'ended_at': match.ended_at.isoformat() if match.ended_at else None
    }
    
    return jsonify({
        'success': True,
        'match': match_data,
        'spectator_count': spectator_count
    })


@spectator_bp.route('/matches/active')
def get_active_matches():
    """Get list of matches that can be spectated"""
    matches = Match.query.filter_by(status='active').order_by(Match.started_at.desc()).limit(20).all()
    
    match_list = []
    for m in matches:
        # Count spectators for this match
        spectator_count = MatchSpectator.query.filter_by(match_id=m.id).count()
        
        match_list.append({
            'id': m.id,
            'status': m.status,
            'started_at': m.started_at.isoformat() if m.started_at else None,
            'challenge_name': m.challenge.title,
            'difficulty': m.challenge.difficulty,
            'player1_name': m.player1.username,
            'player2_name': m.player2.username,
            'spectators': spectator_count
        })
    
    return jsonify(match_list)
