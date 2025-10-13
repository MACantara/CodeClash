from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import sqlite3
import json
import sys
from io import StringIO
import traceback
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['DATABASE'] = 'codeclash.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database"""
    from database import init_database
    init_database()

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
    
    conn = get_db()
    try:
        conn.execute('INSERT INTO users (username) VALUES (?)', (username,))
        conn.commit()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'success': True, 'user_id': user['id']})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'message': 'Username already exists'})
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    """Login existing user"""
    data = request.json
    username = data.get('username')
    
    if not username:
        return jsonify({'success': False, 'message': 'Username is required'})
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({'success': True, 'user_id': user['id']})
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
    conn = get_db()
    users = conn.execute('''
        SELECT username, wins, losses, total_matches, 
               ROUND(CAST(wins AS FLOAT) / NULLIF(total_matches, 0) * 100, 2) as win_rate,
               rating
        FROM users 
        ORDER BY rating DESC, wins DESC
        LIMIT 50
    ''').fetchall()
    conn.close()
    
    return render_template('leaderboard.html', users=users, 
                         current_user=session.get('username'))

@app.route('/challenges')
def get_challenges():
    """Get all available challenges"""
    conn = get_db()
    challenges = conn.execute('SELECT * FROM challenges ORDER BY difficulty').fetchall()
    conn.close()
    
    return jsonify([dict(c) for c in challenges])

@app.route('/match/create', methods=['POST'])
def create_match():
    """Create a new match"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    opponent_username = data.get('opponent')
    challenge_id = data.get('challenge_id')
    
    conn = get_db()
    
    # Get opponent
    opponent = conn.execute('SELECT * FROM users WHERE username = ?', 
                           (opponent_username,)).fetchone()
    
    if not opponent:
        conn.close()
        return jsonify({'success': False, 'message': 'Opponent not found'})
    
    if opponent['id'] == session['user_id']:
        conn.close()
        return jsonify({'success': False, 'message': 'Cannot play against yourself'})
    
    # Create match
    cursor = conn.execute('''
        INSERT INTO matches (player1_id, player2_id, challenge_id, status)
        VALUES (?, ?, ?, 'pending')
    ''', (session['user_id'], opponent['id'], challenge_id))
    
    match_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'match_id': match_id})

@app.route('/match/<int:match_id>')
def match(match_id):
    """Match page"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db()
    match_data = conn.execute('''
        SELECT m.*, c.title, c.description, c.difficulty, c.starter_code, c.test_cases,
               u1.username as player1_name, u2.username as player2_name
        FROM matches m
        JOIN challenges c ON m.challenge_id = c.id
        JOIN users u1 ON m.player1_id = u1.id
        JOIN users u2 ON m.player2_id = u2.id
        WHERE m.id = ?
    ''', (match_id,)).fetchone()
    
    if not match_data:
        conn.close()
        return "Match not found", 404
    
    if session['user_id'] not in [match_data['player1_id'], match_data['player2_id']]:
        conn.close()
        return "Unauthorized", 403
    
    # Start timer when first player enters (change from pending to active)
    if match_data['status'] == 'pending':
        conn.execute('UPDATE matches SET status = "active", started_at = ? WHERE id = ?',
                    (datetime.now(), match_id))
        conn.commit()
        match_data = conn.execute('''
            SELECT m.*, c.title, c.description, c.difficulty, c.starter_code, c.test_cases,
                   u1.username as player1_name, u2.username as player2_name
            FROM matches m
            JOIN challenges c ON m.challenge_id = c.id
            JOIN users u1 ON m.player1_id = u1.id
            JOIN users u2 ON m.player2_id = u2.id
            WHERE m.id = ?
        ''', (match_id,)).fetchone()
    
    conn.close()
    return render_template('match.html', match=dict(match_data), user_id=session['user_id'])

@app.route('/match/<int:match_id>/submit', methods=['POST'])
def submit_solution(match_id):
    """Submit solution for a match"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    code = data.get('code')
    
    conn = get_db()
    match_data = conn.execute('''
        SELECT m.*, c.test_cases, c.time_limit
        FROM matches m
        JOIN challenges c ON m.challenge_id = c.id
        WHERE m.id = ?
    ''', (match_id,)).fetchone()
    
    if not match_data:
        conn.close()
        return jsonify({'success': False, 'message': 'Match not found'})
    
    if session['user_id'] not in [match_data['player1_id'], match_data['player2_id']]:
        conn.close()
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Run test cases
    test_cases = json.loads(match_data['test_cases'])
    results = run_code_tests(code, test_cases)
    
    # Calculate completion time from when match started (when first player entered)
    started_at = datetime.fromisoformat(match_data['started_at']) if match_data['started_at'] else datetime.now()
    completion_time = (datetime.now() - started_at).total_seconds()
    
    # Determine which player submitted
    player_field = 'player1' if session['user_id'] == match_data['player1_id'] else 'player2'
    
    # Update match with submission
    conn.execute(f'''
        UPDATE matches 
        SET {player_field}_code = ?,
            {player_field}_errors = ?,
            {player_field}_time = ?,
            {player_field}_submitted = 1
        WHERE id = ?
    ''', (code, results['errors'], completion_time, match_id))
    
    # Check if both players have submitted
    match_data = conn.execute('SELECT * FROM matches WHERE id = ?', (match_id,)).fetchone()
    
    if match_data['player1_submitted'] and match_data['player2_submitted']:
        # Determine winner
        winner_id = determine_winner(match_data)
        loser_id = match_data['player1_id'] if winner_id == match_data['player2_id'] else match_data['player2_id']
        
        conn.execute('UPDATE matches SET status = "completed", completed_at = ?, winner_id = ? WHERE id = ?',
                    (datetime.now(), winner_id, match_id))
        
        # Update user basic stats
        conn.execute('UPDATE users SET wins = wins + 1, total_matches = total_matches + 1, rating = rating + 25 WHERE id = ?', (winner_id,))
        conn.execute('UPDATE users SET losses = losses + 1, total_matches = total_matches + 1, rating = rating - 10 WHERE id = ?', (loser_id,))
        
        # Update detailed statistics for winner
        winner_errors = match_data['player1_errors'] if winner_id == match_data['player1_id'] else match_data['player2_errors']
        winner_time = match_data['player1_time'] if winner_id == match_data['player1_id'] else match_data['player2_time']
        
        # Check if perfect match
        is_perfect = winner_errors == 0
        
        # Get or create stats
        winner_stats = conn.execute('SELECT * FROM user_statistics WHERE user_id = ?', (winner_id,)).fetchone()
        if not winner_stats:
            conn.execute('INSERT INTO user_statistics (user_id) VALUES (?)', (winner_id,))
            winner_stats = conn.execute('SELECT * FROM user_statistics WHERE user_id = ?', (winner_id,)).fetchone()
        
        # Update win streak
        new_streak = winner_stats['current_win_streak'] + 1
        best_streak = max(new_streak, winner_stats['best_win_streak'])
        
        # Update fastest time
        fastest_time = winner_stats['fastest_solve_time']
        if fastest_time is None or winner_time < fastest_time:
            fastest_time = winner_time
        
        # Update average time
        total_wins = conn.execute('SELECT wins FROM users WHERE id = ?', (winner_id,)).fetchone()['wins']
        avg_time = winner_stats['average_solve_time'] or 0
        new_avg = ((avg_time * (total_wins - 1)) + winner_time) / total_wins if total_wins > 0 else winner_time
        
        conn.execute('''
            UPDATE user_statistics 
            SET current_win_streak = ?,
                best_win_streak = ?,
                fastest_solve_time = ?,
                average_solve_time = ?,
                challenges_solved = challenges_solved + 1,
                perfect_matches = perfect_matches + ?
            WHERE user_id = ?
        ''', (new_streak, best_streak, fastest_time, new_avg, 1 if is_perfect else 0, winner_id))
        
        # Reset loser's win streak
        conn.execute('UPDATE user_statistics SET current_win_streak = 0 WHERE user_id = ?', (loser_id,))
        
        # Check and award achievements
        check_and_award_achievements(winner_id, conn)
        check_and_award_achievements(loser_id, conn)
    
    conn.commit()
    conn.close()
    
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

def determine_winner(match_data):
    """Determine winner based on errors and time"""
    p1_errors = match_data['player1_errors']
    p2_errors = match_data['player2_errors']
    p1_time = match_data['player1_time']
    p2_time = match_data['player2_time']
    
    # Fewer errors wins
    if p1_errors < p2_errors:
        return match_data['player1_id']
    elif p2_errors < p1_errors:
        return match_data['player2_id']
    
    # If errors are equal, faster time wins
    if p1_time < p2_time:
        return match_data['player1_id']
    else:
        return match_data['player2_id']

@app.route('/match/<int:match_id>/status')
def match_status(match_id):
    """Get current match status"""
    conn = get_db()
    match_data = conn.execute('''
        SELECT m.*, u1.username as player1_name, u2.username as player2_name,
               winner.username as winner_name
        FROM matches m
        JOIN users u1 ON m.player1_id = u1.id
        JOIN users u2 ON m.player2_id = u2.id
        LEFT JOIN users winner ON m.winner_id = winner.id
        WHERE m.id = ?
    ''', (match_id,)).fetchone()
    conn.close()
    
    if not match_data:
        return jsonify({'success': False, 'message': 'Match not found'})
    
    return jsonify(dict(match_data))

@app.route('/lobby/list')
def list_lobbies():
    """Get all available lobbies"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    conn = get_db()
    lobbies = conn.execute('''
        SELECT l.*, u.username as host_name, c.title as challenge_name, c.difficulty
        FROM lobbies l
        JOIN users u ON l.host_id = u.id
        JOIN challenges c ON l.challenge_id = c.id
        WHERE l.status = 'waiting' AND l.is_public = 1
        ORDER BY l.created_at DESC
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(lobby) for lobby in lobbies])

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
    
    conn = get_db()
    
    # Check if user already has an active lobby
    existing = conn.execute('''
        SELECT id FROM lobbies 
        WHERE host_id = ? AND status = 'waiting'
    ''', (session['user_id'],)).fetchone()
    
    if existing:
        conn.close()
        return jsonify({'success': False, 'message': 'You already have an active lobby'})
    
    # Create lobby
    cursor = conn.execute('''
        INSERT INTO lobbies (name, host_id, challenge_id, is_public)
        VALUES (?, ?, ?, ?)
    ''', (name, session['user_id'], challenge_id, 1 if is_public else 0))
    
    lobby_id = cursor.lastrowid
    
    # Add host to lobby_players
    conn.execute('''
        INSERT INTO lobby_players (lobby_id, user_id)
        VALUES (?, ?)
    ''', (lobby_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'lobby_id': lobby_id})

@app.route('/lobby/<int:lobby_id>/join', methods=['POST'])
def join_lobby(lobby_id):
    """Join an existing lobby"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    conn = get_db()
    
    # Get lobby info
    lobby = conn.execute('SELECT * FROM lobbies WHERE id = ?', (lobby_id,)).fetchone()
    
    if not lobby:
        conn.close()
        return jsonify({'success': False, 'message': 'Lobby not found'})
    
    if lobby['status'] != 'waiting':
        conn.close()
        return jsonify({'success': False, 'message': 'Lobby is no longer available'})
    
    if lobby['current_players'] >= lobby['max_players']:
        conn.close()
        return jsonify({'success': False, 'message': 'Lobby is full'})
    
    # Check if already in lobby
    already_in = conn.execute('''
        SELECT id FROM lobby_players 
        WHERE lobby_id = ? AND user_id = ?
    ''', (lobby_id, session['user_id'])).fetchone()
    
    if already_in:
        conn.close()
        return jsonify({'success': False, 'message': 'Already in this lobby'})
    
    # Add player to lobby
    conn.execute('''
        INSERT INTO lobby_players (lobby_id, user_id)
        VALUES (?, ?)
    ''', (lobby_id, session['user_id']))
    
    # Update player count
    conn.execute('''
        UPDATE lobbies 
        SET current_players = current_players + 1
        WHERE id = ?
    ''', (lobby_id,))
    
    conn.commit()
    
    # Check if lobby is now full
    lobby = conn.execute('SELECT * FROM lobbies WHERE id = ?', (lobby_id,)).fetchone()
    
    if lobby['current_players'] >= lobby['max_players']:
        # Start match
        match_id = start_match_from_lobby(lobby_id, conn)
        conn.close()
        return jsonify({'success': True, 'lobby_id': lobby_id, 'match_started': True, 'match_id': match_id})
    
    conn.close()
    return jsonify({'success': True, 'lobby_id': lobby_id, 'match_started': False})

@app.route('/lobby/<int:lobby_id>/leave', methods=['POST'])
def leave_lobby(lobby_id):
    """Leave a lobby"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    conn = get_db()
    
    # Get lobby
    lobby = conn.execute('SELECT * FROM lobbies WHERE id = ?', (lobby_id,)).fetchone()
    
    if not lobby:
        conn.close()
        return jsonify({'success': False, 'message': 'Lobby not found'})
    
    # Remove player
    conn.execute('''
        DELETE FROM lobby_players 
        WHERE lobby_id = ? AND user_id = ?
    ''', (lobby_id, session['user_id']))
    
    # Update player count
    conn.execute('''
        UPDATE lobbies 
        SET current_players = current_players - 1
        WHERE id = ?
    ''', (lobby_id,))
    
    # If host left or lobby empty, close lobby
    if lobby['host_id'] == session['user_id']:
        conn.execute('UPDATE lobbies SET status = "closed" WHERE id = ?', (lobby_id,))
    else:
        # Check if lobby is now empty
        remaining = conn.execute('''
            SELECT COUNT(*) as count FROM lobby_players WHERE lobby_id = ?
        ''', (lobby_id,)).fetchone()
        
        if remaining['count'] == 0:
            conn.execute('UPDATE lobbies SET status = "closed" WHERE id = ?', (lobby_id,))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/lobby/<int:lobby_id>/status')
def lobby_status(lobby_id):
    """Get lobby status"""
    conn = get_db()
    
    lobby = conn.execute('''
        SELECT l.*, u.username as host_name, c.title as challenge_name, c.difficulty
        FROM lobbies l
        JOIN users u ON l.host_id = u.id
        JOIN challenges c ON l.challenge_id = c.id
        WHERE l.id = ?
    ''', (lobby_id,)).fetchone()
    
    if not lobby:
        conn.close()
        return jsonify({'success': False, 'message': 'Lobby not found'})
    
    # Get players in lobby
    players = conn.execute('''
        SELECT u.username, lp.joined_at
        FROM lobby_players lp
        JOIN users u ON lp.user_id = u.id
        WHERE lp.lobby_id = ?
        ORDER BY lp.joined_at
    ''', (lobby_id,)).fetchall()
    
    # Check if match exists for this lobby
    match = None
    if lobby['status'] == 'in_match':
        match_data = conn.execute('''
            SELECT id FROM matches WHERE lobby_id = ?
        ''', (lobby_id,)).fetchone()
        if match_data:
            match = match_data['id']
    
    conn.close()
    
    return jsonify({
        'success': True,
        'lobby': dict(lobby),
        'players': [dict(p) for p in players],
        'match_id': match
    })

@app.route('/lobby/quick-match', methods=['POST'])
def quick_match():
    """Find and join an available lobby or create one"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    difficulty = data.get('difficulty', None)
    
    conn = get_db()
    
    # Find available lobby
    query = '''
        SELECT l.id FROM lobbies l
        JOIN challenges c ON l.challenge_id = c.id
        WHERE l.status = 'waiting' 
        AND l.is_public = 1 
        AND l.current_players < l.max_players
        AND l.host_id != ?
    '''
    params = [session['user_id']]
    
    if difficulty:
        query += ' AND c.difficulty = ?'
        params.append(difficulty)
    
    query += ' ORDER BY l.created_at LIMIT 1'
    
    lobby = conn.execute(query, params).fetchone()
    
    if lobby:
        # Join existing lobby
        lobby_id = lobby['id']
        
        # Add player to lobby
        conn.execute('''
            INSERT INTO lobby_players (lobby_id, user_id)
            VALUES (?, ?)
        ''', (lobby_id, session['user_id']))
        
        # Update player count
        conn.execute('''
            UPDATE lobbies 
            SET current_players = current_players + 1
            WHERE id = ?
        ''', (lobby_id,))
        
        conn.commit()
        
        # Check if lobby is now full
        lobby_data = conn.execute('SELECT * FROM lobbies WHERE id = ?', (lobby_id,)).fetchone()
        
        if lobby_data['current_players'] >= lobby_data['max_players']:
            match_id = start_match_from_lobby(lobby_id, conn)
            conn.close()
            return jsonify({'success': True, 'lobby_id': lobby_id, 'match_started': True, 'match_id': match_id})
        
        conn.close()
        return jsonify({'success': True, 'lobby_id': lobby_id, 'match_started': False})
    
    # No lobby found, create one
    # Get random challenge
    query = 'SELECT id FROM challenges'
    params = []
    
    if difficulty:
        query += ' WHERE difficulty = ?'
        params.append(difficulty)
    
    query += ' ORDER BY RANDOM() LIMIT 1'
    
    challenge = conn.execute(query, params).fetchone()
    
    if not challenge:
        conn.close()
        return jsonify({'success': False, 'message': 'No challenges available'})
    
    # Create lobby
    cursor = conn.execute('''
        INSERT INTO lobbies (name, host_id, challenge_id, is_public)
        VALUES (?, ?, ?, 1)
    ''', (f"{session['username']}'s Quick Match", session['user_id'], challenge['id']))
    
    lobby_id = cursor.lastrowid
    
    # Add host to lobby_players
    conn.execute('''
        INSERT INTO lobby_players (lobby_id, user_id)
        VALUES (?, ?)
    ''', (lobby_id, session['user_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'lobby_id': lobby_id, 'created': True, 'match_started': False})

def start_match_from_lobby(lobby_id, conn):
    """Start a match from a full lobby"""
    # Get lobby details
    lobby = conn.execute('SELECT * FROM lobbies WHERE id = ?', (lobby_id,)).fetchone()
    
    # Get players
    players = conn.execute('''
        SELECT user_id FROM lobby_players 
        WHERE lobby_id = ? 
        ORDER BY joined_at 
        LIMIT 2
    ''', (lobby_id,)).fetchall()
    
    if len(players) < 2:
        return None
    
    # Create match
    cursor = conn.execute('''
        INSERT INTO matches (player1_id, player2_id, challenge_id, status, lobby_id)
        VALUES (?, ?, ?, 'pending', ?)
    ''', (players[0]['user_id'], players[1]['user_id'], lobby['challenge_id'], lobby_id))
    
    match_id = cursor.lastrowid
    
    # Update lobby status
    conn.execute('UPDATE lobbies SET status = "in_match" WHERE id = ?', (lobby_id,))
    
    conn.commit()
    
    return match_id

# Import friend routes
from routes_friends import register_friend_routes
register_friend_routes(app, get_db)

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
    
    conn = get_db()
    messages = conn.execute('''
        SELECT cm.*, u.username
        FROM chat_messages cm
        JOIN users u ON cm.user_id = u.id
        WHERE cm.lobby_id = ?
        ORDER BY cm.created_at DESC
        LIMIT 50
    ''', (lobby_id,)).fetchall()
    conn.close()
    
    return jsonify({
        'success': True,
        'messages': [dict(m) for m in reversed(list(messages))]
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
    
    conn = get_db()
    
    # Verify user is in lobby
    in_lobby = conn.execute('''
        SELECT id FROM lobby_players 
        WHERE lobby_id = ? AND user_id = ?
    ''', (lobby_id, session['user_id'])).fetchone()
    
    if not in_lobby:
        conn.close()
        return jsonify({'success': False, 'message': 'Not in lobby'})
    
    conn.execute('''
        INSERT INTO chat_messages (lobby_id, user_id, message)
        VALUES (?, ?, ?)
    ''', (lobby_id, session['user_id'], message))
    conn.commit()
    conn.close()
    
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
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if not user:
        conn.close()
        return "User not found", 404
    
    # Get statistics
    stats = conn.execute('''
        SELECT * FROM user_statistics WHERE user_id = ?
    ''', (user['id'],)).fetchone()
    
    if not stats:
        # Create stats if not exists
        conn.execute('''
            INSERT INTO user_statistics (user_id) VALUES (?)
        ''', (user['id'],))
        conn.commit()
        stats = conn.execute('''
            SELECT * FROM user_statistics WHERE user_id = ?
        ''', (user['id'],)).fetchone()
    
    # Get match history
    matches = conn.execute('''
        SELECT m.*, c.title as challenge_name, c.difficulty,
               u1.username as player1_name,
               u2.username as player2_name,
               winner.username as winner_name
        FROM matches m
        JOIN challenges c ON m.challenge_id = c.id
        JOIN users u1 ON m.player1_id = u1.id
        JOIN users u2 ON m.player2_id = u2.id
        LEFT JOIN users winner ON m.winner_id = winner.id
        WHERE (m.player1_id = ? OR m.player2_id = ?)
          AND m.status = 'completed'
        ORDER BY m.completed_at DESC
        LIMIT 20
    ''', (user['id'], user['id'])).fetchall()
    
    # Get achievements
    achievements = conn.execute('''
        SELECT a.*, ua.earned_at
        FROM user_achievements ua
        JOIN achievements a ON ua.achievement_id = a.id
        WHERE ua.user_id = ?
        ORDER BY ua.earned_at DESC
    ''', (user['id'],)).fetchall()
    
    #Get friends count
    friends_count = conn.execute('''
        SELECT COUNT(*) as count FROM friendships
        WHERE (user_id = ? OR friend_id = ?) AND status = 'accepted'
    ''', (user['id'], user['id'])).fetchone()['count']
    
    conn.close()
    
    return render_template('profile.html', 
                         user=dict(user), 
                         stats=dict(stats),
                         matches=[dict(m) for m in matches],
                         achievements=[dict(a) for a in achievements],
                         friends_count=friends_count,
                         is_own_profile=(session.get('user_id') == user['id']))

# =============== SPECTATOR MODE ROUTES ===============

@app.route('/match/<int:match_id>/spectate')
def spectate_match(match_id):
    """Spectate an ongoing match"""
    if 'user_id' not in session:
        return redirect(url_for('index'))
    
    conn = get_db()
    match_data = conn.execute('''
        SELECT m.*, c.title, c.description, c.difficulty,
               u1.username as player1_name, u2.username as player2_name
        FROM matches m
        JOIN challenges c ON m.challenge_id = c.id
        JOIN users u1 ON m.player1_id = u1.id
        JOIN users u2 ON m.player2_id = u2.id
        WHERE m.id = ? AND m.status IN ('active', 'completed')
    ''', (match_id,)).fetchone()
    
    if not match_data:
        conn.close()
        return "Match not found or not started", 404
    
    # Add as spectator
    existing = conn.execute('''
        SELECT id FROM match_spectators 
        WHERE match_id = ? AND user_id = ?
    ''', (match_id, session['user_id'])).fetchone()
    
    if not existing:
        conn.execute('''
            INSERT INTO match_spectators (match_id, user_id)
            VALUES (?, ?)
        ''', (match_id, session['user_id']))
        conn.commit()
    
    conn.close()
    
    return render_template('spectate.html', match=dict(match_data))

@app.route('/match/<int:match_id>/spectator_data')
def get_spectator_data(match_id):
    """Get match data for spectators"""
    conn = get_db()
    match_data = conn.execute('''
        SELECT m.*, u1.username as player1_name, u2.username as player2_name
        FROM matches m
        JOIN users u1 ON m.player1_id = u1.id
        JOIN users u2 ON m.player2_id = u2.id
        WHERE m.id = ?
    ''', (match_id,)).fetchone()
    
    if not match_data:
        conn.close()
        return jsonify({'success': False, 'message': 'Match not found'})
    
    # Get spectator count
    spectator_count = conn.execute('''
        SELECT COUNT(*) as count FROM match_spectators WHERE match_id = ?
    ''', (match_id,)).fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'success': True,
        'match': dict(match_data),
        'spectator_count': spectator_count
    })

@app.route('/matches/active')
def get_active_matches():
    """Get list of matches that can be spectated"""
    conn = get_db()
    matches = conn.execute('''
        SELECT m.id, m.status, m.started_at,
               c.title as challenge_name, c.difficulty,
               u1.username as player1_name,
               u2.username as player2_name,
               (SELECT COUNT(*) FROM match_spectators WHERE match_id = m.id) as spectators
        FROM matches m
        JOIN challenges c ON m.challenge_id = c.id
        JOIN users u1 ON m.player1_id = u1.id
        JOIN users u2 ON m.player2_id = u2.id
        WHERE m.status = 'active'
        ORDER BY m.started_at DESC
        LIMIT 20
    ''').fetchall()
    conn.close()
    
    return jsonify([dict(m) for m in matches])

# =============== CODE REPLAY ROUTES ===============

@app.route('/match/<int:match_id>/save_snapshot', methods=['POST'])
def save_code_snapshot(match_id):
    """Save code snapshot for replay"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})
    
    data = request.json
    code = data.get('code')
    
    conn = get_db()
    match_data = conn.execute('SELECT * FROM matches WHERE id = ?', (match_id,)).fetchone()
    
    if not match_data:
        conn.close()
        return jsonify({'success': False, 'message': 'Match not found'})
    
    if session['user_id'] not in [match_data['player1_id'], match_data['player2_id']]:
        conn.close()
        return jsonify({'success': False, 'message': 'Unauthorized'})
    
    # Calculate elapsed time
    started_at = datetime.fromisoformat(match_data['started_at']) if match_data['started_at'] else datetime.now()
    elapsed = int((datetime.now() - started_at).total_seconds())
    
    conn.execute('''
        INSERT INTO code_snapshots (match_id, user_id, code, elapsed_seconds)
        VALUES (?, ?, ?, ?)
    ''', (match_id, session['user_id'], code, elapsed))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/match/<int:match_id>/replay')
def view_replay(match_id):
    """View match replay"""
    conn = get_db()
    match_data = conn.execute('''
        SELECT m.*, c.title, c.description, c.difficulty, c.starter_code,
               u1.username as player1_name, u2.username as player2_name,
               winner.username as winner_name
        FROM matches m
        JOIN challenges c ON m.challenge_id = c.id
        JOIN users u1 ON m.player1_id = u1.id
        JOIN users u2 ON m.player2_id = u2.id
        LEFT JOIN users winner ON m.winner_id = winner.id
        WHERE m.id = ? AND m.status = 'completed'
    ''', (match_id,)).fetchone()
    
    if not match_data:
        conn.close()
        return "Match not found or not completed", 404
    
    # Get code snapshots for both players
    player1_snapshots = conn.execute('''
        SELECT * FROM code_snapshots 
        WHERE match_id = ? AND user_id = ?
        ORDER BY elapsed_seconds
    ''', (match_id, match_data['player1_id'])).fetchall()
    
    player2_snapshots = conn.execute('''
        SELECT * FROM code_snapshots 
        WHERE match_id = ? AND user_id = ?
        ORDER BY elapsed_seconds
    ''', (match_id, match_data['player2_id'])).fetchall()
    
    conn.close()
    
    return render_template('replay.html',
                         match=dict(match_data),
                         player1_snapshots=[dict(s) for s in player1_snapshots],
                         player2_snapshots=[dict(s) for s in player2_snapshots])

# =============== ACHIEVEMENTS HELPER ===============

def check_and_award_achievements(user_id, conn):
    """Check and award achievements for a user"""
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    stats = conn.execute('SELECT * FROM user_statistics WHERE user_id = ?', (user_id,)).fetchone()
    
    if not stats:
        return
    
    achievements_to_award = []
    
    # First win
    if user['wins'] == 1:
        achievements_to_award.append('first_win')
    
    # Win streak
    if stats['current_win_streak'] >= 5:
        achievements_to_award.append('win_streak_5')
    
    # Perfect match
    if stats['perfect_matches'] > 0:
        achievements_to_award.append('perfect_match')
    
    # Veteran
    if user['total_matches'] >= 50:
        achievements_to_award.append('play_50_matches')
    
    # Master
    if user['wins'] >= 100:
        achievements_to_award.append('win_100')
    
    # Award achievements
    for criteria in achievements_to_award:
        achievement = conn.execute('''
            SELECT id FROM achievements WHERE criteria = ?
        ''', (criteria,)).fetchone()
        
        if achievement:
            # Check if already awarded
            existing = conn.execute('''
                SELECT id FROM user_achievements 
                WHERE user_id = ? AND achievement_id = ?
            ''', (user_id, achievement['id'])).fetchone()
            
            if not existing:
                conn.execute('''
                    INSERT INTO user_achievements (user_id, achievement_id)
                    VALUES (?, ?)
                ''', (user_id, achievement['id']))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True, port=5000)
