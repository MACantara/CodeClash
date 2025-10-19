"""
Database seeding script for CodeClash
Seeds challenges and achievements into the database
Loads data from JSON files in the data/ directory
"""
from models import db, Challenge, Achievement
import json
import os
import glob

def load_json_files(pattern):
    """Load JSON files matching the pattern"""
    files = sorted(glob.glob(pattern))
    data = []
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data.append(json.load(f))
    return data

def seed_challenges():
    """Seed initial challenges from JSON files"""
    print("Loading challenges from JSON files...")
    challenges_data = load_json_files('data/challenges/*.json')
    
    for challenge_data in challenges_data:
        # Check if challenge already exists
        existing = Challenge.query.filter_by(title=challenge_data['title']).first()
        if not existing:
            # Convert test_cases list to JSON string for database
            challenge_data['test_cases'] = json.dumps(challenge_data['test_cases'])
            challenge = Challenge(**challenge_data)
            db.session.add(challenge)
    
    db.session.commit()
    print(f"✅ Seeded {len(challenges_data)} challenges")

def seed_achievements():
    """Seed achievements from JSON files"""
    print("Loading achievements from JSON files...")
    achievements_data = load_json_files('data/achievements/*.json')
    
    for achievement_data in achievements_data:
        # Check if achievement already exists
        existing = Achievement.query.filter_by(name=achievement_data['name']).first()
        if not existing:
            # Convert criteria dict to JSON string for database
            achievement_data['criteria'] = json.dumps(achievement_data['criteria'])
            achievement = Achievement(**achievement_data)
            db.session.add(achievement)
    
    db.session.commit()
    print(f"✅ Seeded {len(achievements_data)} achievements")

def seed_all():
    """Seed all data"""
    seed_challenges()
    seed_achievements()
    print("\n🎉 Database seeding completed!")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        seed_all()