"""Lobby routes (list, create, join, leave, status, quick-match)"""
from flask import Blueprint, request, jsonify, session
from models import db, Lobby, LobbyPlayer, Challenge
from utils import start_match_from_lobby

lobby_bp = Blueprint('lobby', __name__)


@lobby_bp.route('/lobby/list')
def list_lobbies():
    """Get all available lobbies"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    lobbies = Lobby.query.filter_by(status='waiting', is_public=True).order_by(Lobby.created_at.desc()).all()
    
    lobby_list = []
    for lobby in lobbies:
        lobby_list.append({
            'id': lobby.id,
            'name': lobby.name,
            'host_id': lobby.host_id,
            'host_name': lobby.host.username,
            'challenge_id': lobby.challenge_id,
            'challenge_name': lobby.challenge.title,
            'difficulty': lobby.challenge.difficulty,
            'current_players': lobby.current_players,
            'max_players': lobby.max_players,
            'is_public': lobby.is_public,
            'status': lobby.status,
            'created_at': lobby.created_at.isoformat() if lobby.created_at else None
        })
    
    return jsonify(lobby_list)


@lobby_bp.route('/lobby/create', methods=['POST'])
def create_lobby():
    """Create a new lobby"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    name = data.get('name', f"{session['username']}'s Room")
    challenge_id = data.get('challenge_id')
    is_public = data.get('is_public', True)
    
    if not challenge_id:
        return jsonify({'success': False, 'message': 'Challenge is required'})
    
    # Check if user already has an active lobby
    existing = Lobby.query.filter_by(
        host_id=session['user_id'],
        status='waiting'
    ).first()
    
    if existing:
        return jsonify({'success': False, 'message': 'You already have an active lobby'})
    
    # Create lobby
    lobby = Lobby(
        name=name,
        host_id=session['user_id'],
        challenge_id=challenge_id,
        is_public=is_public,
        current_players=1  # Initialize with 1 player (the host)
    )
    db.session.add(lobby)
    db.session.flush()  # Get the lobby ID
    
    # Add host to lobby_players
    lobby_player = LobbyPlayer(
        lobby_id=lobby.id,
        user_id=session['user_id']
    )
    db.session.add(lobby_player)
    
    db.session.commit()
    
    return jsonify({'success': True, 'lobby_id': lobby.id})


@lobby_bp.route('/lobby/<int:lobby_id>/join', methods=['POST'])
def join_lobby(lobby_id):
    """Join an existing lobby"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    # Get lobby info
    lobby = db.session.get(Lobby, lobby_id)
    
    if not lobby:
        return jsonify({'success': False, 'message': 'Lobby not found'})
    
    if lobby.status != 'waiting':
        return jsonify({'success': False, 'message': 'Lobby is no longer available'})
    
    if lobby.current_players >= lobby.max_players:
        return jsonify({'success': False, 'message': 'Lobby is full'})
    
    # Check if already in lobby
    already_in = LobbyPlayer.query.filter_by(
        lobby_id=lobby_id,
        user_id=session['user_id']
    ).first()
    
    if already_in:
        return jsonify({'success': False, 'message': 'Already in this lobby'})
    
    # Add player to lobby
    lobby_player = LobbyPlayer(
        lobby_id=lobby_id,
        user_id=session['user_id']
    )
    db.session.add(lobby_player)
    
    # Update player count
    lobby.current_players += 1
    
    db.session.commit()
    
    # Check if lobby is now full
    if lobby.current_players >= lobby.max_players:
        # Start match
        match_id = start_match_from_lobby(lobby_id)
        return jsonify({'success': True, 'lobby_id': lobby_id, 'match_started': True, 'match_id': match_id})
    
    return jsonify({'success': True, 'lobby_id': lobby_id, 'match_started': False})


@lobby_bp.route('/lobby/<int:lobby_id>/leave', methods=['POST'])
def leave_lobby(lobby_id):
    """Leave a lobby"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    # Get lobby
    lobby = db.session.get(Lobby, lobby_id)
    
    if not lobby:
        return jsonify({'success': False, 'message': 'Lobby not found'})
    
    # Remove player
    LobbyPlayer.query.filter_by(
        lobby_id=lobby_id,
        user_id=session['user_id']
    ).delete()
    
    # Update player count
    lobby.current_players -= 1
    
    # If host left or lobby empty, close lobby
    if lobby.host_id == session['user_id']:
        lobby.status = 'closed'
    else:
        # Check if lobby is now empty
        remaining = LobbyPlayer.query.filter_by(lobby_id=lobby_id).count()
        
        if remaining == 0:
            lobby.status = 'closed'
    
    db.session.commit()
    
    return jsonify({'success': True})


@lobby_bp.route('/lobby/<int:lobby_id>/status')
def lobby_status(lobby_id):
    """Get lobby status"""
    lobby = db.session.get(Lobby, lobby_id)
    
    if not lobby:
        return jsonify({'success': False, 'message': 'Lobby not found'})
    
    # Get players in lobby
    lobby_players = LobbyPlayer.query.filter_by(lobby_id=lobby_id).order_by(LobbyPlayer.joined_at).all()
    
    players = []
    for lp in lobby_players:
        players.append({
            'username': lp.user.username,
            'joined_at': lp.joined_at.isoformat() if lp.joined_at else None
        })
    
    # Check if match exists for this lobby
    match_id = None
    if lobby.status == 'in_match' and lobby.match_id:
        # Use the lobby's match_id field (proper relationship)
        match_id = lobby.match_id
    
    lobby_data = {
        'id': lobby.id,
        'name': lobby.name,
        'host_id': lobby.host_id,
        'host_name': lobby.host.username,
        'challenge_id': lobby.challenge_id,
        'challenge_name': lobby.challenge.title,
        'difficulty': lobby.challenge.difficulty,
        'current_players': lobby.current_players,
        'max_players': lobby.max_players,
        'is_public': lobby.is_public,
        'status': lobby.status,
        'created_at': lobby.created_at.isoformat() if lobby.created_at else None
    }
    
    return jsonify({
        'success': True,
        'lobby': lobby_data,
        'players': players,
        'match_id': match_id
    })


@lobby_bp.route('/lobby/quick-match', methods=['POST'])
def quick_match():
    """Find and join an available lobby or create one"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    difficulty = data.get('difficulty', None)
    
    # Check if user is already in a lobby
    existing_lobby_player = LobbyPlayer.query.filter_by(user_id=session['user_id']).first()
    if existing_lobby_player:
        existing_lobby = db.session.get(Lobby, existing_lobby_player.lobby_id)
        if existing_lobby and existing_lobby.status == 'waiting':
            return jsonify({'success': True, 'lobby_id': existing_lobby.id, 'already_in_lobby': True, 'match_started': False})
    
    # Find available lobby (prioritize oldest lobbies first)
    query = Lobby.query.join(Challenge).filter(
        Lobby.status == 'waiting',
        Lobby.is_public == True,
        Lobby.current_players < Lobby.max_players,
        Lobby.host_id != session['user_id']  # Don't join your own lobby
    )
    
    if difficulty:
        query = query.filter(Challenge.difficulty == difficulty)
    
    # Order by created_at ASC to join the oldest (first created) lobby
    lobby = query.order_by(Lobby.created_at.asc()).first()
    
    if lobby:
        # Join existing lobby
        lobby_id = lobby.id
        
        # Add player to lobby
        lobby_player = LobbyPlayer(
            lobby_id=lobby_id,
            user_id=session['user_id']
        )
        db.session.add(lobby_player)
        
        # Update player count
        lobby.current_players += 1
        
        db.session.commit()
        
        # Check if lobby is now full
        if lobby.current_players >= lobby.max_players:
            match_id = start_match_from_lobby(lobby_id)
            return jsonify({'success': True, 'lobby_id': lobby_id, 'match_started': True, 'match_id': match_id})
        
        return jsonify({'success': True, 'lobby_id': lobby_id, 'match_started': False})
    
    # No lobby found, create one
    # Get random challenge
    query = Challenge.query
    
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    
    challenge = query.order_by(db.func.random()).first()
    
    if not challenge:
        return jsonify({'success': False, 'message': 'No challenges available'})
    
    # Create lobby
    new_lobby = Lobby(
        name=f"{session['username']}'s Quick Match",
        host_id=session['user_id'],
        challenge_id=challenge.id,
        is_public=True,
        current_players=1  # Initialize with 1 player (the host)
    )
    db.session.add(new_lobby)
    db.session.flush()  # Get the lobby ID
    
    # Add host to lobby_players
    lobby_player = LobbyPlayer(
        lobby_id=new_lobby.id,
        user_id=session['user_id']
    )
    db.session.add(lobby_player)
    
    db.session.commit()
    
    return jsonify({'success': True, 'lobby_id': new_lobby.id, 'created': True, 'match_started': False})
