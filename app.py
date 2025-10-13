from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import json
import sys
from io import StringIO
import traceback

# Import config and models
from config import create_app
from models import db, User, Challenge, Match, Lobby, LobbyPlayer, Friendship, LobbyInvitation, ChatMessage, MatchSpectator, CodeSnapshot, Achievement, UserAchievement, UserStatistics

# Create app using factory
app = create_app()

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/register', methods=['POST'])
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

@app.route('/login', methods=['POST'])
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

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/tournament')
def tournament():
    """Tournament page - redirect to lobby"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return redirect(url_for('lobby'))

@app.route('/lobby')
def lobby():
    """Lobby page with matchmaking"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('lobby.html', username=session['username'])

@app.route('/leaderboard')
def leaderboard():
    """Leaderboard page"""
    users = User.query.order_by(User.rating.desc(), User.wins.desc()).limit(50).all()
    
    # Add win_rate calculation
    users_data = []
    for user in users:
        user_dict = {
            'username': user.username,
            'wins': user.wins,
            'losses': user.losses,
            'total_matches': user.total_matches,
            'rating': user.rating,
            'win_rate': round((user.wins / user.total_matches * 100) if user.total_matches > 0 else 0, 2)
        }
        users_data.append(user_dict)
    
    return render_template('leaderboard.html', users=users_data, 
                         current_user=session.get('username'))

@app.route('/challenges')
def get_challenges():
    """Get all available challenges"""
    challenges = Challenge.query.order_by(Challenge.difficulty).all()
    
    challenges_data = []
    for c in challenges:
        challenges_data.append({
            'id': c.id,
            'title': c.title,
            'description': c.description,
            'difficulty': c.difficulty,
            'starter_code': c.starter_code,
            'test_cases': c.test_cases,
            'time_limit': c.time_limit
        })
    
    return jsonify(challenges_data)

@app.route('/match/create', methods=['POST'])
def create_match():
    """Create a new match"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    opponent_username = data.get('opponent')
    challenge_id = data.get('challenge_id')
    
    # Get opponent
    opponent = User.query.filter_by(username=opponent_username).first()
    
    if not opponent:
        return jsonify({'success': False, 'message': 'Opponent not found'})
    
    if opponent.id == session['user_id']:
        return jsonify({'success': False, 'message': 'Cannot play against yourself'})
    
    try:
        # Create match
        match = Match(
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

@app.route('/match/<int:match_id>')
def match(match_id):
    """Match page"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    match_obj = db.session.get(Match, match_id)
    
    if not match_obj:
        return "Match not found", 404
    
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
        'started_at': match_obj.started_at.isoformat() if match_obj.started_at else None,
        'title': match_obj.challenge.title,
        'description': match_obj.challenge.description,
        'difficulty': match_obj.challenge.difficulty,
        'starter_code': match_obj.challenge.starter_code,
        'test_cases': match_obj.challenge.test_cases,
        'player1_name': match_obj.player1.username,
        'player2_name': match_obj.player2.username
    }
    
    return render_template('match.html', match=match_data, user_id=session['user_id'])

@app.route('/match/<int:match_id>/submit', methods=['POST'])
def submit_solution(match_id):
    """Submit solution for a match"""
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
    
    # Calculate completion time from when match started (when first player entered)
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
    
    # Check if both players have submitted
    
    if match_obj.player1_submitted and match_obj.player2_submitted:
        # Determine winner
        winner_id = determine_winner(match_obj)
        loser_id = match_obj.player1_id if winner_id == match_obj.player2_id else match_obj.player2_id
        
        # Update match status
        match_obj.status = 'completed'
        match_obj.completed_at = datetime.utcnow()
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
            db.session.flush()  # Get the stats object with default values
        
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

def run_code_tests(code, test_cases):
    """Run code against test cases"""
    passed = 0
    total = len(test_cases)
    errors = 0
    details = []
    
    for test in test_cases:
        try:
            # Capture stdout
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            # Create a namespace for execution
            namespace = {}
            exec(code, namespace)
            
            # Get the function to test (assume it's the first function defined)
            func_name = test['function']
            if func_name not in namespace:
                raise Exception(f"Function '{func_name}' not found")
            
            func = namespace[func_name]
            
            # Run the test
            result = func(*test['input'])
            output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            # Check result
            if result == test['expected']:
                passed += 1
                details.append({
                    'input': test['input'],
                    'expected': test['expected'],
                    'actual': result,
                    'passed': True
                })
            else:
                errors += 1
                details.append({
                    'input': test['input'],
                    'expected': test['expected'],
                    'actual': result,
                    'passed': False,
                    'error': 'Output mismatch'
                })
        except Exception as e:
            sys.stdout = old_stdout
            errors += 1
            details.append({
                'input': test.get('input', []),
                'expected': test.get('expected', None),
                'actual': None,
                'passed': False,
                'error': str(e)
            })
    
    return {
        'passed': passed,
        'total': total,
        'errors': errors,
        'details': details
    }

def determine_winner(match_obj):
    """Determine winner based on errors and time"""
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

@app.route('/match/<int:match_id>/status')
def match_status(match_id):
    """Get current match status"""
    match = db.session.get(Match, match_id)
    
    if not match:
        return jsonify({'success': False, 'message': 'Match not found'})
    
    # Build response with player names via relationships
    match_data = {
        'id': match.id,
        'challenge_id': match.challenge_id,
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
        'completed_at': match.completed_at.isoformat() if match.completed_at else None,
        'winner_id': match.winner_id,
        'winner_name': match.winner.username if match.winner else None
    }
    
    return jsonify(match_data)

@app.route('/lobby/list')
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

@app.route('/lobby/create', methods=['POST'])
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

@app.route('/lobby/<int:lobby_id>/join', methods=['POST'])
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

@app.route('/lobby/<int:lobby_id>/leave', methods=['POST'])
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

@app.route('/lobby/<int:lobby_id>/status')
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
    if lobby.status == 'in_match':
        match = Match.query.filter_by(lobby_id=lobby_id).first()
        if match:
            match_id = match.id
    
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

@app.route('/lobby/quick-match', methods=['POST'])
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

def start_match_from_lobby(lobby_id):
    """Start a match from a full lobby"""
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
        status='pending',
        lobby_id=lobby_id
    )
    db.session.add(match)
    db.session.flush()  # Get the match ID
    
    # Update lobby status
    lobby.status = 'in_match'
    
    db.session.commit()
    
    return match.id

# Import friend routes
from routes_friends import register_friend_routes
register_friend_routes(app)

@app.route('/friends')
def friends_page():
    """Render friends page"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('friends.html')

@app.route('/matches')
def matches_page():
    """Render active matches page"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('matches.html')

# =============== CHAT ROUTES ===============

@app.route('/lobby/<int:lobby_id>/messages')
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

@app.route('/lobby/<int:lobby_id>/send_message', methods=['POST'])
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

# =============== MATCH HISTORY & PROFILE ROUTES ===============

@app.route('/profile')
@app.route('/profile/<username>')
def user_profile(username=None):
    """View user profile with stats"""
    if username is None:
        if 'username' not in session:
            return redirect(url_for('index'))
        username = session['username']
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return "User not found", 404
    
    # Get statistics
    stats = user.statistics
    
    if not stats:
        # Create stats if not exists
        stats = UserStatistics(user_id=user.id)
        db.session.add(stats)
        db.session.commit()
    
    # Get match history
    matches = Match.query.filter(
        db.or_(Match.player1_id == user.id, Match.player2_id == user.id),
        Match.status == 'completed'
    ).order_by(Match.completed_at.desc()).limit(20).all()
    
    match_list = []
    for m in matches:
        match_list.append({
            'id': m.id,
            'challenge_name': m.challenge.title,
            'difficulty': m.challenge.difficulty,
            'player1_name': m.player1.username,
            'player2_name': m.player2.username,
            'winner_name': m.winner.username if m.winner else None,
            'winner_id': m.winner_id,
            'completed_at': m.completed_at.isoformat() if m.completed_at else None,
            'status': m.status
        })
    
    # Get achievements
    user_achievements = UserAchievement.query.filter_by(user_id=user.id).order_by(UserAchievement.earned_at.desc()).all()
    
    achievement_list = []
    for ua in user_achievements:
        achievement_list.append({
            'id': ua.achievement.id,
            'name': ua.achievement.name,
            'description': ua.achievement.description,
            'criteria': ua.achievement.criteria,
            'icon': ua.achievement.icon,
            'earned_at': ua.earned_at.isoformat() if ua.earned_at else None
        })
    
    # Get friends count
    friends_count = Friendship.query.filter(
        db.or_(Friendship.user_id == user.id, Friendship.friend_id == user.id),
        Friendship.status == 'accepted'
    ).count()
    
    # Convert stats to dict
    stats_dict = {
        'user_id': stats.user_id,
        'current_win_streak': stats.current_win_streak,
        'best_win_streak': stats.best_win_streak,
        'fastest_solve_time': stats.fastest_solve_time,
        'average_solve_time': stats.average_solve_time,
        'challenges_solved': stats.challenges_solved,
        'perfect_matches': stats.perfect_matches
    }
    
    user_dict = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'rating': user.rating,
        'wins': user.wins,
        'losses': user.losses,
        'total_matches': user.total_matches,
        'created_at': user.created_at.isoformat() if user.created_at else None
    }
    
    return render_template('profile.html', 
                         user=user_dict, 
                         stats=stats_dict,
                         matches=match_list,
                         achievements=achievement_list,
                         friends_count=friends_count,
                         is_own_profile=(session.get('user_id') == user.id))

# =============== SPECTATOR MODE ROUTES ===============

@app.route('/match/<int:match_id>/spectate')
def spectate_match(match_id):
    """Spectate an ongoing match"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
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
        'title': match.challenge.title,
        'description': match.challenge.description,
        'difficulty': match.challenge.difficulty,
        'player1_name': match.player1.username,
        'player2_name': match.player2.username,
        'status': match.status,
        'player1_submitted': match.player1_submitted,
        'player2_submitted': match.player2_submitted
    }
    
    return render_template('spectate.html', match=match_data)

@app.route('/match/<int:match_id>/spectator_data')
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
        'status': match.status,
        'player1_submitted': match.player1_submitted,
        'player2_submitted': match.player2_submitted,
        'player1_errors': match.player1_errors,
        'player2_errors': match.player2_errors,
        'started_at': match.started_at.isoformat() if match.started_at else None,
        'completed_at': match.completed_at.isoformat() if match.completed_at else None
    }
    
    return jsonify({
        'success': True,
        'match': match_data,
        'spectator_count': spectator_count
    })

@app.route('/matches/active')
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

# =============== CODE REPLAY ROUTES ===============

@app.route('/match/<int:match_id>/save_snapshot', methods=['POST'])
def save_code_snapshot(match_id):
    """Save code snapshot for replay"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    code = data.get('code')
    
    match = db.session.get(Match, match_id)
    
    if not match:
        return jsonify({'success': False, 'message': 'Match not found'})
    
    if session['user_id'] not in [match.player1_id, match.player2_id]:
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Calculate elapsed time
    started_at = match.started_at if match.started_at else datetime.utcnow()
    elapsed = int((datetime.utcnow() - started_at).total_seconds())
    
    snapshot = CodeSnapshot(
        match_id=match_id,
        user_id=session['user_id'],
        code=code,
        elapsed_seconds=elapsed
    )
    db.session.add(snapshot)
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/match/<int:match_id>/replay')
def view_replay(match_id):
    """View match replay"""
    match = Match.query.filter_by(id=match_id, status='completed').first()
    
    if not match:
        return "Match not found or not completed", 404
    
    # Get code snapshots for both players
    player1_snapshots = CodeSnapshot.query.filter_by(
        match_id=match_id,
        user_id=match.player1_id
    ).order_by(CodeSnapshot.elapsed_seconds).all()
    
    player2_snapshots = CodeSnapshot.query.filter_by(
        match_id=match_id,
        user_id=match.player2_id
    ).order_by(CodeSnapshot.elapsed_seconds).all()
    
    match_data = {
        'id': match.id,
        'title': match.challenge.title,
        'description': match.challenge.description,
        'difficulty': match.challenge.difficulty,
        'starter_code': match.challenge.starter_code,
        'player1_name': match.player1.username,
        'player2_name': match.player2.username,
        'winner_name': match.winner.username if match.winner else None,
        'player1_code': match.player1_code,
        'player2_code': match.player2_code,
        'status': match.status
    }
    
    player1_snapshot_list = [{
        'id': s.id,
        'code': s.code,
        'elapsed_seconds': s.elapsed_seconds,
        'created_at': s.created_at.isoformat() if s.created_at else None
    } for s in player1_snapshots]
    
    player2_snapshot_list = [{
        'id': s.id,
        'code': s.code,
        'elapsed_seconds': s.elapsed_seconds,
        'created_at': s.created_at.isoformat() if s.created_at else None
    } for s in player2_snapshots]
    
    return render_template('replay.html',
                         match=match_data,
                         player1_snapshots=player1_snapshot_list,
                         player2_snapshots=player2_snapshot_list)

# =============== ACHIEVEMENTS HELPER ===============

def check_and_award_achievements(user_id):
    """Check and award achievements for a user"""
    user = db.session.get(User, user_id)
    stats = user.statistics
    
    if not stats:
        return
    
    achievements_to_award = []
    
    # First win
    if user.wins == 1:
        achievements_to_award.append('first_win')
    
    # Win streak
    if stats.current_win_streak >= 5:
        achievements_to_award.append('win_streak_5')
    
    # Perfect match
    if stats.perfect_matches > 0:
        achievements_to_award.append('perfect_match')
    
    # Veteran
    if user.total_matches >= 50:
        achievements_to_award.append('play_50_matches')
    
    # Master
    if user.wins >= 100:
        achievements_to_award.append('win_100')
    
    # Award achievements
    for criteria in achievements_to_award:
        achievement = Achievement.query.filter_by(criteria=criteria).first()
        
        if achievement:
            # Check if already awarded
            existing = UserAchievement.query.filter_by(
                user_id=user_id,
                achievement_id=achievement.id
            ).first()
            
            if not existing:
                user_achievement = UserAchievement(
                    user_id=user_id,
                    achievement_id=achievement.id
                )
                db.session.add(user_achievement)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
