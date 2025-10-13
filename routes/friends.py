"""Friend routes (list, add, accept, reject, remove)"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from sqlalchemy import or_, and_
from models import db, User, Friendship

friends_bp = Blueprint('friends', __name__)


@friends_bp.route('/friends')
def friends_page():
    """Render friends page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
    return render_template('friends.html')


@friends_bp.route('/friends/list')
def list_friends():
    """Get list of friends and friend requests"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    user_id = session['user_id']
    
    # Get all friendships (both directions)
    friendships = Friendship.query.filter(
        or_(Friendship.user_id == user_id, Friendship.friend_id == user_id)
    ).all()
    
    friends = []
    pending_sent = []
    pending_received = []
    
    for friendship in friendships:
        # Determine the other user
        if friendship.user_id == user_id:
            friend_id = friendship.friend_id
            is_sender = True
        else:
            friend_id = friendship.user_id
            is_sender = False
        
        friend = db.session.get(User, friend_id)
        
        if not friend:
            continue
        
        friend_data = {
            'id': friend.id,
            'username': friend.username,
            'rating': friend.rating,
            'wins': friend.wins,
            'losses': friend.losses,
            'friendship_id': friendship.id,
            'status': friendship.status
        }
        
        if friendship.status == 'accepted':
            friends.append(friend_data)
        elif friendship.status == 'pending':
            if is_sender:
                pending_sent.append(friend_data)
            else:
                pending_received.append(friend_data)
    
    return jsonify({
        'success': True,
        'friends': friends,
        'pending_sent': pending_sent,
        'pending_received': pending_received
    })


@friends_bp.route('/friends/add', methods=['POST'])
def add_friend():
    """Send friend request"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    friend_username = data.get('username')
    
    if not friend_username:
        return jsonify({'success': False, 'message': 'Username is required'})
    
    # Get friend user
    friend = User.query.filter_by(username=friend_username).first()
    
    if not friend:
        return jsonify({'success': False, 'message': 'User not found'})
    
    if friend.id == session['user_id']:
        return jsonify({'success': False, 'message': 'Cannot add yourself'})
    
    # Check if friendship already exists (in either direction)
    existing = Friendship.query.filter(
        or_(
            and_(Friendship.user_id == session['user_id'], Friendship.friend_id == friend.id),
            and_(Friendship.user_id == friend.id, Friendship.friend_id == session['user_id'])
        )
    ).first()
    
    if existing:
        return jsonify({'success': False, 'message': 'Friend request already exists'})
    
    # Create friendship
    friendship = Friendship(
        user_id=session['user_id'],
        friend_id=friend.id,
        status='pending'
    )
    db.session.add(friendship)
    db.session.commit()
    
    return jsonify({'success': True})


@friends_bp.route('/friends/accept/<int:friendship_id>', methods=['POST'])
def accept_friend(friendship_id):
    """Accept friend request"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    friendship = db.session.get(Friendship, friendship_id)
    
    if not friendship:
        return jsonify({'success': False, 'message': 'Friend request not found'})
    
    # Verify this user is the receiver
    if friendship.friend_id != session['user_id']:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    friendship.status = 'accepted'
    db.session.commit()
    
    return jsonify({'success': True})


@friends_bp.route('/friends/reject/<int:friendship_id>', methods=['POST'])
def reject_friend(friendship_id):
    """Reject friend request"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    friendship = db.session.get(Friendship, friendship_id)
    
    if not friendship:
        return jsonify({'success': False, 'message': 'Friend request not found'})
    
    # Verify this user is the receiver
    if friendship.friend_id != session['user_id']:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    db.session.delete(friendship)
    db.session.commit()
    
    return jsonify({'success': True})


@friends_bp.route('/friends/remove/<int:friend_id>', methods=['POST'])
def remove_friend(friend_id):
    """Remove friend"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    # Find friendship (could be in either direction)
    friendship = Friendship.query.filter(
        or_(
            and_(Friendship.user_id == session['user_id'], Friendship.friend_id == friend_id),
            and_(Friendship.user_id == friend_id, Friendship.friend_id == session['user_id'])
        )
    ).first()
    
    if not friendship:
        return jsonify({'success': False, 'message': 'Friendship not found'})
    
    db.session.delete(friendship)
    db.session.commit()
    
    return jsonify({'success': True})
