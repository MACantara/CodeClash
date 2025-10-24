"""Page routes"""
from flask import Blueprint, render_template

pages_bp = Blueprint('pages', __name__)


@pages_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@pages_bp.route('/challenges')
def challenges_list():
    """Challenges list page"""
    return render_template('challenges_list.html')
