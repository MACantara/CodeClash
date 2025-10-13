"""Match helper utilities"""
from datetime import datetime
from models import db, Match, Lobby, LobbyPlayer


def determine_winner(match_obj):
    """
    Determine winner based on errors and time.
    
    Args:
        match_obj: Match object
        
    Returns:
        Winner's user ID
    """
    p1_errors = match_obj.player1_errors
    p2_errors = match_obj.player2_errors
    p1_time = match_obj.player1_time
    p2_time = match_obj.player2_time
    
    # Fewer errors wins
    if p1_errors < p2_errors:
        return match_obj.player1_id
    elif p2_errors < p1_errors:
        return match_obj.player2_id
    
    # If errors are equal, faster time wins
    if p1_time < p2_time:
        return match_obj.player1_id
    else:
        return match_obj.player2_id


def start_match_from_lobby(lobby_id):
    """
    Start a match from a full lobby.
    
    Args:
        lobby_id: ID of the lobby to start match from
        
    Returns:
        Match ID if successful, None otherwise
    """
    # Get lobby details
    lobby = db.session.get(Lobby, lobby_id)
    
    # Get players
    players = LobbyPlayer.query.filter_by(lobby_id=lobby_id).order_by(LobbyPlayer.joined_at).limit(2).all()
    
    if len(players) < 2:
        return None
    
    # Create match
    match = Match(
        player1_id=players[0].user_id,
        player2_id=players[1].user_id,
        challenge_id=lobby.challenge_id,
        status='pending'
    )
    db.session.add(match)
    db.session.flush()  # Get the match ID
    
    # Update lobby status and link to match
    lobby.status = 'in_match'
    lobby.match_id = match.id  # Set the lobby's match_id field
    
    db.session.commit()
    
    return match.id
