"""Page routes (tournament, lobby page, matches page)"""
from flask import Blueprint, render_template, session, redirect, url_for

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/tournament')
def tournament():
    """Tournament page - redirect to lobby"""
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
    return redirect(url_for('pages.lobby_page'))


@pages_bp.route('/lobby')
def lobby_page():
    """Lobby page with matchmaking"""
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
    return render_template('lobby.html', username=session['username'])


@pages_bp.route('/matches')
def matches_page():
    """Render active matches page"""
    if 'user_id' not in session:
        return redirect(url_for('auth.index'))
    return render_template('matches.html')
