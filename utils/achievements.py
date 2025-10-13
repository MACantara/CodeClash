"""Achievement checking and awarding utilities"""
from models import db, User, Achievement, UserAchievement


def check_and_award_achievements(user_id):
    """
    Check and award achievements for a user.
    
    Args:
        user_id: ID of the user to check achievements for
    """
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
