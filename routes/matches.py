"""Match routes (create, view, submit, status)"""
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from models import db, Match

matches_bp = Blueprint('matches', __name__)


@matches_bp.route('/match/create', methods=['POST'])
def create_match():
    """Create a new practice match"""
    data = request.json
    challenge_id = data.get('challenge_id')
    
    if not challenge_id:
        return jsonify({'success': False, 'message': 'Challenge is required'})
    
    try:
        match = Match(
            challenge_id=challenge_id,
            status='active',
            started_at=datetime.utcnow()
        )
        db.session.add(match)
        db.session.commit()
        
        return jsonify({'success': True, 'match_id': match.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@matches_bp.route('/match/<int:match_id>')
def match(match_id):
    """Match page - Code execution disabled"""
    match_obj = db.session.get(Match, match_id)
    
    if not match_obj:
        return "Match not found", 404
    
    # Code execution has been disabled for security reasons
    # Display match information only
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Match {match_id} - CodeClash</title>
        <style>
            body {{ 
                font-family: Arial, sans-serif; 
                max-width: 800px; 
                margin: 50px auto; 
                padding: 20px;
                background-color: #1a1a2e;
                color: #eee;
            }}
            .card {{ 
                background: #16213e; 
                padding: 30px; 
                border-radius: 10px;
                border: 1px solid #0f3460;
            }}
            h1 {{ color: #4a9eff; }}
            .info {{ margin: 15px 0; }}
            .label {{ font-weight: bold; color: #4a9eff; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Match #{match_id}</h1>
            <div class="info">
                <span class="label">Challenge:</span> {match_obj.challenge.title}
            </div>
            <div class="info">
                <span class="label">Description:</span> {match_obj.challenge.description}
            </div>
            <div class="info">
                <span class="label">Difficulty:</span> {match_obj.challenge.difficulty}
            </div>
            <div class="info">
                <span class="label">Status:</span> {match_obj.status}
            </div>
            <p style="margin-top: 30px; color: #aaa; font-style: italic;">
                Note: Code execution has been disabled for security reasons.
            </p>
            <a href="/" style="color: #4a9eff; text-decoration: none;">← Back to Home</a>
        </div>
    </body>
    </html>
    """


@matches_bp.route('/match/<int:match_id>/status')
def match_status(match_id):
    """Get current match status"""
    match = db.session.get(Match, match_id)
    
    if not match:
        return jsonify({'success': False, 'message': 'Match not found'})
    
    match_data = {
        'id': match.id,
        'challenge_id': match.challenge_id,
        'player_submitted': match.player_submitted,
        'player_errors': match.player_errors,
        'player_time': match.player_time,
        'status': match.status,
        'created_at': match.created_at.isoformat() if match.created_at else None,
        'started_at': match.started_at.isoformat() if match.started_at else None,
        'ended_at': match.ended_at.isoformat() if match.ended_at else None,
    }
    
    return jsonify(match_data)
