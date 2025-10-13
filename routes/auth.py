"""Authentication routes (register, login, logout)"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import db, User, UserStatistics

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'success': False, 'message': 'Username is required'})
    
    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'success': False, 'message': 'Username already exists'})
    
    try:
        # Create new user (password_hash can be empty for now, or set a default)
        user = User(username=username, password_hash='')
        db.session.add(user)
        db.session.commit()
        
        # Create user statistics entry
        stats = UserStatistics(user_id=user.id)
        db.session.add(stats)
        db.session.commit()
        
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({'success': True, 'user_id': user.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login existing user"""
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'success': False, 'message': 'Username is required'})
    
    user = User.query.filter_by(username=username).first()
    
    if user:
        session['user_id'] = user.id
        session['username'] = user.username
        return jsonify({'success': True, 'user_id': user.id})
    else:
        return jsonify({'success': False, 'message': 'User not found'})


@auth_bp.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('auth.index'))
