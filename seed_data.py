"""
Database seeding script for CodeClash
Seeds challenges and achievements into the database
"""
from models import db, Challenge, Achievement
import json

def seed_challenges():
    """Seed initial challenges"""
    challenges_data = [
        # Easy Challenges
        {
            'title': 'Sum of Two Numbers',
            'description': 'Write a function called `add_numbers(a, b)` that returns the sum of two numbers.',
            'difficulty': 'Easy',
            'starter_code': 'def add_numbers(a, b):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': [2, 3], 'expected': 5},
                {'input': [10, 20], 'expected': 30},
                {'input': [-5, 5], 'expected': 0},
                {'input': [0, 0], 'expected': 0}
            ]),
            'time_limit': 300
        },
        {
            'title': 'Reverse a String',
            'description': 'Write a function called `reverse_string(s)` that returns the reversed version of the input string.',
            'difficulty': 'Easy',
            'starter_code': 'def reverse_string(s):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': ['hello'], 'expected': 'olleh'},
                {'input': ['Python'], 'expected': 'nohtyP'},
                {'input': [''], 'expected': ''},
                {'input': ['a'], 'expected': 'a'}
            ]),
            'time_limit': 300
        },
        {
            'title': 'Find Maximum',
            'description': 'Write a function called `find_max(numbers)` that returns the maximum number in a list.',
            'difficulty': 'Easy',
            'starter_code': 'def find_max(numbers):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': [[1, 5, 3, 9, 2]], 'expected': 9},
                {'input': [[-1, -5, -3]], 'expected': -1},
                {'input': [[42]], 'expected': 42},
                {'input': [[0, 0, 0]], 'expected': 0}
            ]),
            'time_limit': 300
        },
        # Medium Challenges
        {
            'title': 'Check Palindrome',
            'description': 'Write a function called `is_palindrome(s)` that returns True if the string is a palindrome, False otherwise. Ignore case and spaces.',
            'difficulty': 'Medium',
            'starter_code': 'def is_palindrome(s):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': ['racecar'], 'expected': True},
                {'input': ['hello'], 'expected': False},
                {'input': ['A man a plan a canal Panama'], 'expected': True},
                {'input': [''], 'expected': True}
            ]),
            'time_limit': 300
        },
        {
            'title': 'Fibonacci Sequence',
            'description': 'Write a function called `fibonacci(n)` that returns the nth Fibonacci number (0-indexed).',
            'difficulty': 'Medium',
            'starter_code': 'def fibonacci(n):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': [0], 'expected': 0},
                {'input': [1], 'expected': 1},
                {'input': [5], 'expected': 5},
                {'input': [10], 'expected': 55}
            ]),
            'time_limit': 300
        },
        {
            'title': 'Two Sum',
            'description': 'Write a function called `two_sum(nums, target)` that returns indices of two numbers that add up to the target.',
            'difficulty': 'Medium',
            'starter_code': 'def two_sum(nums, target):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': [[2, 7, 11, 15], 9], 'expected': [0, 1]},
                {'input': [[3, 2, 4], 6], 'expected': [1, 2]},
                {'input': [[3, 3], 6], 'expected': [0, 1]}
            ]),
            'time_limit': 300
        },
        # Hard Challenges
        {
            'title': 'Valid Parentheses',
            'description': 'Write a function called `is_valid(s)` that returns True if the parentheses string is valid (properly opened and closed).',
            'difficulty': 'Hard',
            'starter_code': 'def is_valid(s):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': ['()'], 'expected': True},
                {'input': ['()[]{}'], 'expected': True},
                {'input': ['(]'], 'expected': False},
                {'input': ['([)]'], 'expected': False},
                {'input': ['{[]}'], 'expected': True}
            ]),
            'time_limit': 300
        },
        {
            'title': 'Merge Sorted Arrays',
            'description': 'Write a function called `merge_sorted(arr1, arr2)` that merges two sorted arrays into one sorted array.',
            'difficulty': 'Hard',
            'starter_code': 'def merge_sorted(arr1, arr2):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': [[1, 3, 5], [2, 4, 6]], 'expected': [1, 2, 3, 4, 5, 6]},
                {'input': [[1, 2, 3], [4, 5, 6]], 'expected': [1, 2, 3, 4, 5, 6]},
                {'input': [[], [1, 2, 3]], 'expected': [1, 2, 3]},
                {'input': [[1], [2]], 'expected': [1, 2]}
            ]),
            'time_limit': 300
        }
    ]
    
    for challenge_data in challenges_data:
        # Check if challenge already exists
        existing = Challenge.query.filter_by(title=challenge_data['title']).first()
        if not existing:
            challenge = Challenge(**challenge_data)
            db.session.add(challenge)
    
    db.session.commit()
    print(f"Seeded {len(challenges_data)} challenges")

def seed_achievements():
    """Seed achievements"""
    achievements_data = [
        {
            'name': 'First Blood',
            'description': 'Win your first match',
            'icon': 'bi-trophy-fill',
            'points': 10,
            'criteria': json.dumps({'type': 'wins', 'value': 1})
        },
        {
            'name': 'Winning Streak',
            'description': 'Win 5 matches in a row',
            'icon': 'bi-fire',
            'points': 25,
            'criteria': json.dumps({'type': 'win_streak', 'value': 5})
        },
        {
            'name': 'Perfect Game',
            'description': 'Win 3 matches with zero errors',
            'icon': 'bi-star-fill',
            'points': 30,
            'criteria': json.dumps({'type': 'perfect_matches', 'value': 3})
        },
        {
            'name': 'Speed Demon',
            'description': 'Solve a challenge in under 30 seconds',
            'icon': 'bi-lightning-charge-fill',
            'points': 20,
            'criteria': json.dumps({'type': 'fastest_time', 'value': 30})
        },
        {
            'name': 'Veteran',
            'description': 'Complete 50 matches',
            'icon': 'bi-shield-fill',
            'points': 15,
            'criteria': json.dumps({'type': 'total_matches', 'value': 50})
        },
        {
            'name': 'Master Coder',
            'description': 'Solve 10 different challenges',
            'icon': 'bi-code-slash',
            'points': 50,
            'criteria': json.dumps({'type': 'unique_challenges', 'value': 10})
        },
        {
            'name': 'Challenge Accepted',
            'description': 'Complete at least one challenge of each difficulty',
            'icon': 'bi-trophy',
            'points': 40,
            'criteria': json.dumps({'type': 'all_difficulties', 'value': True})
        },
        {
            'name': 'Social Butterfly',
            'description': 'Add 10 friends',
            'icon': 'bi-people-fill',
            'points': 15,
            'criteria': json.dumps({'type': 'friends', 'value': 10})
        },
        {
            'name': 'Comeback King',
            'description': 'Win after losing 3 matches in a row',
            'icon': 'bi-arrow-up-circle-fill',
            'points': 25,
            'criteria': json.dumps({'type': 'comeback', 'value': 3})
        },
        {
            'name': 'No Mercy',
            'description': 'Win 10 matches in a row',
            'icon': 'bi-lightning-fill',
            'points': 35,
            'criteria': json.dumps({'type': 'win_streak', 'value': 10})
        }
    ]
    
    for achievement_data in achievements_data:
        # Check if achievement already exists
        existing = Achievement.query.filter_by(name=achievement_data['name']).first()
        if not existing:
            achievement = Achievement(**achievement_data)
            db.session.add(achievement)
    
    db.session.commit()
    print(f"Seeded {len(achievements_data)} achievements")

def seed_all():
    """Seed all data"""
    seed_challenges()
    seed_achievements()
    print("Database seeding completed!")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        seed_all()
