"""Match routes (create, view, submit, status) - IndexedDB client-side storage"""
from flask import Blueprint, render_template, request, jsonify
from datetime import datetime

matches_bp = Blueprint('matches', __name__)


@matches_bp.route('/match/create', methods=['POST'])
def create_match():
    """Create a new practice match - now handled client-side with IndexedDB"""
    data = request.json
    challenge_id = data.get('challenge_id')
    
    if not challenge_id:
        return jsonify({'success': False, 'message': 'Challenge is required'})
    
    # Return success - actual match creation happens client-side in IndexedDB
    # Generate a client-side ID (timestamp-based)
    match_id = int(datetime.utcnow().timestamp() * 1000)
    
    return jsonify({
        'success': True, 
        'match_id': match_id,
        'message': 'Match will be created in browser storage'
    })


@matches_bp.route('/match/<int:match_id>')
def match(match_id):
    """Match page - Code execution disabled, data stored in IndexedDB"""
    # Just return a simple page that uses IndexedDB to load match data
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Match {match_id} - CodeClash</title>
        <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">
    </head>
    <body class="bg-gray-900 text-gray-100">
        <div class="container mx-auto px-4 py-8">
            <div class="max-w-4xl mx-auto">
                <div class="bg-gray-800 rounded-lg shadow-xl p-6 border border-gray-700">
                    <h1 class="text-3xl font-bold mb-4 text-blue-500">
                        <i class="bi bi-flag-fill"></i> Match #{match_id}
                    </h1>
                    <div id="matchData" class="space-y-4">
                        <p class="text-gray-400">Loading match data from browser storage...</p>
                    </div>
                    <div class="mt-6">
                        <a href="/" class="text-blue-500 hover:text-blue-400">
                            <i class="bi bi-arrow-left"></i> Back to Home
                        </a>
                    </div>
                </div>
            </div>
        </div>
        
        <script src="/static/js/db.js"></script>
        <script>
            async function loadMatchData() {{
                try {{
                    await initDB();
                    const match = await MatchDB.getById({match_id});
                    
                    if (match) {{
                        const challenge = await ChallengeDB.getById(match.challenge_id);
                        
                        document.getElementById('matchData').innerHTML = `
                            <div class="space-y-3">
                                <div>
                                    <span class="font-bold text-blue-400">Challenge:</span> 
                                    <span class="text-gray-300">${{challenge ? challenge.title : 'Unknown'}}</span>
                                </div>
                                <div>
                                    <span class="font-bold text-blue-400">Description:</span> 
                                    <span class="text-gray-300">${{challenge ? challenge.description : 'N/A'}}</span>
                                </div>
                                <div>
                                    <span class="font-bold text-blue-400">Difficulty:</span> 
                                    <span class="px-2 py-1 rounded text-sm ${{
                                        challenge && challenge.difficulty === 'Easy' ? 'bg-green-600' :
                                        challenge && challenge.difficulty === 'Medium' ? 'bg-yellow-600' : 'bg-red-600'
                                    }}">${{challenge ? challenge.difficulty : 'N/A'}}</span>
                                </div>
                                <div>
                                    <span class="font-bold text-blue-400">Status:</span> 
                                    <span class="text-gray-300">${{match.status}}</span>
                                </div>
                                <div>
                                    <span class="font-bold text-blue-400">Started:</span> 
                                    <span class="text-gray-300">${{new Date(match.started_at).toLocaleString()}}</span>
                                </div>
                                <p class="mt-6 text-gray-500 italic border-t border-gray-700 pt-4">
                                    <i class="bi bi-info-circle"></i> Note: Code execution has been disabled for security reasons.
                                    All data is stored locally in your browser using IndexedDB.
                                </p>
                            </div>
                        `;
                    }} else {{
                        document.getElementById('matchData').innerHTML = `
                            <p class="text-red-400">
                                <i class="bi bi-exclamation-triangle"></i> Match not found in local storage.
                            </p>
                        `;
                    }}
                }} catch (error) {{
                    console.error('Error loading match:', error);
                    document.getElementById('matchData').innerHTML = `
                        <p class="text-red-400">
                            <i class="bi bi-exclamation-triangle"></i> Error loading match data: ${{error.message}}
                        </p>
                    `;
                }}
            }}
            
            loadMatchData();
        </script>
    </body>
    </html>
    """


@matches_bp.route('/match/<int:match_id>/status')
def match_status(match_id):
    """Get current match status - returns placeholder, actual data in IndexedDB"""
    return jsonify({
        'success': True,
        'message': 'Match data stored in IndexedDB client-side',
        'match_id': match_id
    })

