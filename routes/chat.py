"""Chat routes (lobby messages)"""
from flask import Blueprint, request, jsonify, session
from models import db, ChatMessage, LobbyPlayer

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/lobby/<int:lobby_id>/messages')
def get_lobby_messages(lobby_id):
    """Get chat messages for a lobby"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    messages = ChatMessage.query.filter_by(lobby_id=lobby_id).order_by(ChatMessage.created_at.desc()).limit(50).all()
    
    message_list = []
    for msg in reversed(messages):
        message_list.append({
            'id': msg.id,
            'lobby_id': msg.lobby_id,
            'user_id': msg.user_id,
            'username': msg.user.username,
            'message': msg.message,
            'created_at': msg.created_at.isoformat() if msg.created_at else None
        })
    
    return jsonify({
        'success': True,
        'messages': message_list
    })


@chat_bp.route('/lobby/<int:lobby_id>/send_message', methods=['POST'])
def send_lobby_message(lobby_id):
    """Send a chat message in lobby"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    message = data.get('message', '').strip()
    
    if not message or len(message) > 500:
        return jsonify({'success': False, 'message': 'Invalid message'})
    
    # Verify user is in lobby
    in_lobby = LobbyPlayer.query.filter_by(
        lobby_id=lobby_id,
        user_id=session['user_id']
    ).first()
    
    if not in_lobby:
        return jsonify({'success': False, 'message': 'Not in lobby'})
    
    chat_message = ChatMessage(
        lobby_id=lobby_id,
        user_id=session['user_id'],
        message=message
    )
    db.session.add(chat_message)
    db.session.commit()
    
    return jsonify({'success': True})
