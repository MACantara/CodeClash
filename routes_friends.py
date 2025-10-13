# Friends System Routes

from flask import session, jsonify, request
from datetime import datetime
from models import db, User, Friendship
from sqlalchemy import or_, and_

def register_friend_routes(app):
    """Register all friend-related routes"""
    
    @app.route('/friends/list')
    def list_friends():
        """Get user's friends list"""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        # Get accepted friendships
        friendships = Friendship.query.filter(
            or_(Friendship.user_id == session['user_id'], Friendship.friend_id == session['user_id']),
            Friendship.status == 'accepted'
        ).all()
        
        friends = []
        for f in friendships:
            # Get the other user (not the current user)
            friend_id = f.friend_id if f.user_id == session['user_id'] else f.user_id
            friend_user = db.session.get(User, friend_id)
            friends.append({
                'id': friend_user.id,
                'username': friend_user.username,
                'rating': friend_user.rating,
                'wins': friend_user.wins,
                'losses': friend_user.losses,
                'friends_since': f.created_at.isoformat() if f.created_at else None
            })
        
        # Sort by username
        friends.sort(key=lambda x: x['username'])
        
        # Get pending requests sent by current user
        pending_sent_requests = Friendship.query.filter_by(
            user_id=session['user_id'],
            status='pending'
        ).all()
        
        pending_sent = []
        for f in pending_sent_requests:
            friend_user = db.session.get(User, f.friend_id)
            pending_sent.append({
                'id': friend_user.id,
                'username': friend_user.username,
                'created_at': f.created_at.isoformat() if f.created_at else None
            })
        
        # Get pending requests received by current user
        pending_received_requests = Friendship.query.filter_by(
            friend_id=session['user_id'],
            status='pending'
        ).all()
        
        pending_received = []
        for f in pending_received_requests:
            sender_user = db.session.get(User, f.user_id)
            pending_received.append({
                'id': sender_user.id,
                'username': sender_user.username,
                'request_id': f.id,
                'created_at': f.created_at.isoformat() if f.created_at else None
            })
        
        return jsonify({
            'success': True,
            'friends': friends,
            'pending_sent': pending_sent,
            'pending_received': pending_received
        })
    
    @app.route('/friends/add', methods=['POST'])
    def add_friend():
        """Send friend request"""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        data = request.json
        friend_username = data.get('username')
        
        if not friend_username:
            return jsonify({'success': False, 'message': 'Username required'})
        
        friend = User.query.filter_by(username=friend_username).first()
        
        if not friend:
            return jsonify({'success': False, 'message': 'User not found'})
        
        if friend.id == session['user_id']:
            return jsonify({'success': False, 'message': 'Cannot add yourself'})
        
        # Check if already friends or request exists
        existing = Friendship.query.filter(
            or_(
                and_(Friendship.user_id == session['user_id'], Friendship.friend_id == friend.id),
                and_(Friendship.user_id == friend.id, Friendship.friend_id == session['user_id'])
            )
        ).first()
        
        if existing:
            return jsonify({'success': False, 'message': 'Friend request already exists'})
        
        # Create friend request
        friendship = Friendship(
            user_id=session['user_id'],
            friend_id=friend.id,
            status='pending'
        )
        db.session.add(friendship)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Friend request sent!'})
    
    @app.route('/friends/accept/<int:request_id>', methods=['POST'])
    def accept_friend(request_id):
        """Accept friend request"""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        friendship = Friendship.query.filter_by(
            id=request_id,
            friend_id=session['user_id']
        ).first()
        
        if not friendship:
            return jsonify({'success': False, 'message': 'Request not found'})
        
        friendship.status = 'accepted'
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Friend request accepted!'})
    
    @app.route('/friends/reject/<int:request_id>', methods=['POST'])
    def reject_friend(request_id):
        """Reject friend request"""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        friendship = Friendship.query.filter_by(
            id=request_id,
            friend_id=session['user_id']
        ).first()
        
        if not friendship:
            return jsonify({'success': False, 'message': 'Request not found'})
        
        db.session.delete(friendship)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Friend request rejected'})
    
    @app.route('/friends/remove/<int:friend_id>', methods=['POST'])
    def remove_friend(friend_id):
        """Remove friend"""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        Friendship.query.filter(
            or_(
                and_(Friendship.user_id == session['user_id'], Friendship.friend_id == friend_id),
                and_(Friendship.user_id == friend_id, Friendship.friend_id == session['user_id'])
            ),
            Friendship.status == 'accepted'
        ).delete()
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Friend removed'})
