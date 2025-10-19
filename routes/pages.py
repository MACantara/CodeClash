"""Page routes (lobby page)"""
from flask import Blueprint, render_template, session, redirect, url_for

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/lobby')
def lobby_page():
    """Lobby page with matchmaking"""
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
    return render_template('lobby.html', username=session['username'])
