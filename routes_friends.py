# Friends System Routes

from flask import session, jsonify, request
from datetime import datetime

def register_friend_routes(app, get_db):
    """Register all friend-related routes"""
    
    @app.route('/friends/list')
    def list_friends():
        """Get user's friends list"""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        conn = get_db()
        friends = conn.execute('''
            SELECT u.id, u.username, u.rating, u.wins, u.losses,
                   f.created_at as friends_since
            FROM friendships f
            JOIN users u ON (f.friend_id = u.id OR f.user_id = u.id)
            WHERE (f.user_id = ? OR f.friend_id = ?)
              AND f.status = 'accepted'
              AND u.id != ?
            ORDER BY u.username
        ''', (session['user_id'], session['user_id'], session['user_id'])).fetchall()
        
        # Get pending requests
        pending_sent = conn.execute('''
            SELECT u.id, u.username, f.created_at
            FROM friendships f
            JOIN users u ON f.friend_id = u.id
            WHERE f.user_id = ? AND f.status = 'pending'
        ''', (session['user_id'],)).fetchall()
        
        pending_received = conn.execute('''
            SELECT u.id, u.username, f.id as request_id, f.created_at
            FROM friendships f
            JOIN users u ON f.user_id = u.id
            WHERE f.friend_id = ? AND f.status = 'pending'
        ''', (session['user_id'],)).fetchall()
        
        conn.close()
        
        return jsonify({
            'success': True,
            'friends': [dict(f) for f in friends],
            'pending_sent': [dict(p) for p in pending_sent],
            'pending_received': [dict(p) for p in pending_received]
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
        
        conn = get_db()
        friend = conn.execute('SELECT * FROM users WHERE username = ?', 
                             (friend_username,)).fetchone()
        
        if not friend:
            conn.close()
            return jsonify({'success': False, 'message': 'User not found'})
        
        if friend['id'] == session['user_id']:
            conn.close()
            return jsonify({'success': False, 'message': 'Cannot add yourself'})
        
        # Check if already friends or request exists
        existing = conn.execute('''
            SELECT * FROM friendships 
            WHERE (user_id = ? AND friend_id = ?) 
               OR (user_id = ? AND friend_id = ?)
        ''', (session['user_id'], friend['id'], friend['id'], session['user_id'])).fetchone()
        
        if existing:
            conn.close()
            return jsonify({'success': False, 'message': 'Friend request already exists'})
        
        # Create friend request
        conn.execute('''
            INSERT INTO friendships (user_id, friend_id, status)
            VALUES (?, ?, 'pending')
        ''', (session['user_id'], friend['id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Friend request sent!'})
    
    @app.route('/friends/accept/<int:request_id>', methods=['POST'])
    def accept_friend(request_id):
        """Accept friend request"""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        conn = get_db()
        request_data = conn.execute('''
            SELECT * FROM friendships WHERE id = ? AND friend_id = ?
        ''', (request_id, session['user_id'])).fetchone()
        
        if not request_data:
            conn.close()
            return jsonify({'success': False, 'message': 'Request not found'})
        
        conn.execute('''
            UPDATE friendships SET status = 'accepted' WHERE id = ?
        ''', (request_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Friend request accepted!'})
    
    @app.route('/friends/reject/<int:request_id>', methods=['POST'])
    def reject_friend(request_id):
        """Reject friend request"""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        conn = get_db()
        request_data = conn.execute('''
            SELECT * FROM friendships WHERE id = ? AND friend_id = ?
        ''', (request_id, session['user_id'])).fetchone()
        
        if not request_data:
            conn.close()
            return jsonify({'success': False, 'message': 'Request not found'})
        
        conn.execute('DELETE FROM friendships WHERE id = ?', (request_id,))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Friend request rejected'})
    
    @app.route('/friends/remove/<int:friend_id>', methods=['POST'])
    def remove_friend(friend_id):
        """Remove friend"""
        if 'user_id' not in session:
            return jsonify({'success': False, 'message': 'Not logged in'})
        
        conn = get_db()
        conn.execute('''
            DELETE FROM friendships 
            WHERE ((user_id = ? AND friend_id = ?) 
                OR (user_id = ? AND friend_id = ?))
              AND status = 'accepted'
        ''', (session['user_id'], friend_id, friend_id, session['user_id']))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Friend removed'})
