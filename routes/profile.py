"""Profile and leaderboard routes"""
from flask import Blueprint, render_template, session, redirect, url_for
from models import db, User, Match, UserAchievement

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/leaderboard')
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


@profile_bp.route('/profile')
@profile_bp.route('/profile/<username>')
def user_profile(username=None):
    """View user profile with stats"""
    if username is None:
        if 'username' not in session:
            return redirect(url_for('auth.index'))
        username = session['username']
    
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return "User not found", 404
    
    # Get statistics
    stats = user.statistics
    
    if not stats:
        from models import UserStatistics
        # Create stats if not exists
        stats = UserStatistics(user_id=user.id)
        db.session.add(stats)
        db.session.commit()
    
    # Get match history
    matches = Match.query.filter(
        db.or_(Match.player1_id == user.id, Match.player2_id == user.id),
        Match.status == 'completed'
    ).order_by(Match.ended_at.desc()).limit(20).all()
    
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
            'ended_at': m.ended_at.isoformat() if m.ended_at else None,
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
                         is_own_profile=(session.get('user_id') == user.id))
