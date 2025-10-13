import sqlite3
import json

def init_database():
    """Initialize the database with tables and sample data"""
    conn = sqlite3.connect('codeclash.db')
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0,
            total_matches INTEGER DEFAULT 0,
            rating INTEGER DEFAULT 1000,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create challenges table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            difficulty TEXT NOT NULL,
            starter_code TEXT,
            test_cases TEXT NOT NULL,
            time_limit INTEGER DEFAULT 300,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create matches table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player1_id INTEGER NOT NULL,
            player2_id INTEGER NOT NULL,
            challenge_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            player1_code TEXT,
            player2_code TEXT,
            player1_errors INTEGER DEFAULT 0,
            player2_errors INTEGER DEFAULT 0,
            player1_time REAL DEFAULT 0,
            player2_time REAL DEFAULT 0,
            player1_submitted INTEGER DEFAULT 0,
            player2_submitted INTEGER DEFAULT 0,
            winner_id INTEGER,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            lobby_id INTEGER,
            FOREIGN KEY (player1_id) REFERENCES users(id),
            FOREIGN KEY (player2_id) REFERENCES users(id),
            FOREIGN KEY (challenge_id) REFERENCES challenges(id),
            FOREIGN KEY (winner_id) REFERENCES users(id),
            FOREIGN KEY (lobby_id) REFERENCES lobbies(id)
        )
    ''')
    
    # Create lobbies table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lobbies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            host_id INTEGER NOT NULL,
            challenge_id INTEGER NOT NULL,
            difficulty_filter TEXT,
            max_players INTEGER DEFAULT 2,
            current_players INTEGER DEFAULT 1,
            status TEXT DEFAULT 'waiting',
            is_public INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (host_id) REFERENCES users(id),
            FOREIGN KEY (challenge_id) REFERENCES challenges(id)
        )
    ''')
    
    # Create lobby_players table for tracking players in lobbies
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lobby_players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lobby_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lobby_id) REFERENCES lobbies(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create friends table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS friendships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            friend_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (friend_id) REFERENCES users(id)
        )
    ''')
    
    # Create lobby_invitations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lobby_invitations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lobby_id INTEGER NOT NULL,
            from_user_id INTEGER NOT NULL,
            to_user_id INTEGER NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lobby_id) REFERENCES lobbies(id),
            FOREIGN KEY (from_user_id) REFERENCES users(id),
            FOREIGN KEY (to_user_id) REFERENCES users(id)
        )
    ''')
    
    # Create chat_messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lobby_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lobby_id) REFERENCES lobbies(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create match_spectators table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS match_spectators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (match_id) REFERENCES matches(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create code_snapshots table for replay feature
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            match_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            elapsed_seconds INTEGER,
            FOREIGN KEY (match_id) REFERENCES matches(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Create achievements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            criteria TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create user_achievements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            achievement_id INTEGER NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (achievement_id) REFERENCES achievements(id)
        )
    ''')
    
    # Create user_statistics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_statistics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL UNIQUE,
            current_win_streak INTEGER DEFAULT 0,
            best_win_streak INTEGER DEFAULT 0,
            total_errors INTEGER DEFAULT 0,
            fastest_solve_time REAL,
            average_solve_time REAL,
            challenges_solved INTEGER DEFAULT 0,
            perfect_matches INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Add achievements if they don't exist
    cursor.execute('SELECT COUNT(*) FROM achievements')
    if cursor.fetchone()[0] == 0:
        achievements = [
            ('First Blood', 'Win your first match', 'bi-trophy', 'first_win', 10),
            ('Winning Streak', 'Win 5 matches in a row', 'bi-fire', 'win_streak_5', 50),
            ('Perfect Game', 'Win a match with zero errors', 'bi-star-fill', 'perfect_match', 25),
            ('Speed Demon', 'Solve a challenge in under 60 seconds', 'bi-lightning-charge-fill', 'solve_under_60', 30),
            ('Veteran', 'Play 50 matches', 'bi-shield-fill', 'play_50_matches', 40),
            ('Master Coder', 'Win 100 matches', 'bi-award-fill', 'win_100', 100),
            ('Challenge Accepted', 'Complete all difficulty levels', 'bi-check-circle-fill', 'all_difficulties', 75),
            ('Social Butterfly', 'Add 10 friends', 'bi-people-fill', 'add_10_friends', 20),
            ('Comeback King', 'Win after being behind', 'bi-arrow-up-circle-fill', 'comeback_win', 35),
            ('No Mercy', 'Win by more than 10 errors difference', 'bi-x-circle-fill', 'dominate_win', 40),
        ]
        cursor.executemany('''
            INSERT INTO achievements (name, description, icon, criteria, points)
            VALUES (?, ?, ?, ?, ?)
        ''', achievements)
    
    # Check if challenges already exist
    cursor.execute('SELECT COUNT(*) FROM challenges')
    if cursor.fetchone()[0] == 0:
        # Add sample challenges
        challenges = [
            {
                'title': 'Sum of Two Numbers',
                'description': 'Write a function that takes two numbers and returns their sum.',
                'difficulty': 'Easy',
                'starter_code': 'def sum_two_numbers(a, b):\n    # Write your code here\n    pass',
                'test_cases': json.dumps([
                    {'function': 'sum_two_numbers', 'input': [1, 2], 'expected': 3},
                    {'function': 'sum_two_numbers', 'input': [5, 7], 'expected': 12},
                    {'function': 'sum_two_numbers', 'input': [-3, 3], 'expected': 0},
                    {'function': 'sum_two_numbers', 'input': [0, 0], 'expected': 0},
                ])
            },
            {
                'title': 'Reverse a String',
                'description': 'Write a function that takes a string and returns it reversed.',
                'difficulty': 'Easy',
                'starter_code': 'def reverse_string(s):\n    # Write your code here\n    pass',
                'test_cases': json.dumps([
                    {'function': 'reverse_string', 'input': ['hello'], 'expected': 'olleh'},
                    {'function': 'reverse_string', 'input': ['Python'], 'expected': 'nohtyP'},
                    {'function': 'reverse_string', 'input': [''], 'expected': ''},
                    {'function': 'reverse_string', 'input': ['a'], 'expected': 'a'},
                ])
            },
            {
                'title': 'Find Maximum',
                'description': 'Write a function that takes a list of numbers and returns the maximum value.',
                'difficulty': 'Easy',
                'starter_code': 'def find_max(numbers):\n    # Write your code here\n    pass',
                'test_cases': json.dumps([
                    {'function': 'find_max', 'input': [[1, 5, 3, 9, 2]], 'expected': 9},
                    {'function': 'find_max', 'input': [[-1, -5, -3]], 'expected': -1},
                    {'function': 'find_max', 'input': [[42]], 'expected': 42},
                    {'function': 'find_max', 'input': [[0, 0, 0]], 'expected': 0},
                ])
            },
            {
                'title': 'Palindrome Checker',
                'description': 'Write a function that checks if a string is a palindrome (reads the same forwards and backwards).',
                'difficulty': 'Medium',
                'starter_code': 'def is_palindrome(s):\n    # Write your code here\n    pass',
                'test_cases': json.dumps([
                    {'function': 'is_palindrome', 'input': ['racecar'], 'expected': True},
                    {'function': 'is_palindrome', 'input': ['hello'], 'expected': False},
                    {'function': 'is_palindrome', 'input': ['a'], 'expected': True},
                    {'function': 'is_palindrome', 'input': [''], 'expected': True},
                ])
            },
            {
                'title': 'Fibonacci Number',
                'description': 'Write a function that returns the nth Fibonacci number (0-indexed).',
                'difficulty': 'Medium',
                'starter_code': 'def fibonacci(n):\n    # Write your code here\n    pass',
                'test_cases': json.dumps([
                    {'function': 'fibonacci', 'input': [0], 'expected': 0},
                    {'function': 'fibonacci', 'input': [1], 'expected': 1},
                    {'function': 'fibonacci', 'input': [5], 'expected': 5},
                    {'function': 'fibonacci', 'input': [10], 'expected': 55},
                ])
            },
            {
                'title': 'Two Sum',
                'description': 'Given a list of integers and a target, return indices of two numbers that add up to the target.',
                'difficulty': 'Medium',
                'starter_code': 'def two_sum(nums, target):\n    # Write your code here\n    # Return a list of two indices\n    pass',
                'test_cases': json.dumps([
                    {'function': 'two_sum', 'input': [[2, 7, 11, 15], 9], 'expected': [0, 1]},
                    {'function': 'two_sum', 'input': [[3, 2, 4], 6], 'expected': [1, 2]},
                    {'function': 'two_sum', 'input': [[3, 3], 6], 'expected': [0, 1]},
                ])
            },
            {
                'title': 'Valid Parentheses',
                'description': 'Write a function to check if a string of parentheses is valid. Valid means every opening bracket has a corresponding closing bracket in the correct order.',
                'difficulty': 'Hard',
                'starter_code': 'def is_valid_parentheses(s):\n    # Write your code here\n    pass',
                'test_cases': json.dumps([
                    {'function': 'is_valid_parentheses', 'input': ['()'], 'expected': True},
                    {'function': 'is_valid_parentheses', 'input': ['()[]{}'], 'expected': True},
                    {'function': 'is_valid_parentheses', 'input': ['(]'], 'expected': False},
                    {'function': 'is_valid_parentheses', 'input': ['([)]'], 'expected': False},
                    {'function': 'is_valid_parentheses', 'input': ['{[]}'], 'expected': True},
                ])
            },
            {
                'title': 'Merge Sorted Arrays',
                'description': 'Write a function that merges two sorted arrays into one sorted array.',
                'difficulty': 'Hard',
                'starter_code': 'def merge_sorted(arr1, arr2):\n    # Write your code here\n    pass',
                'test_cases': json.dumps([
                    {'function': 'merge_sorted', 'input': [[1, 3, 5], [2, 4, 6]], 'expected': [1, 2, 3, 4, 5, 6]},
                    {'function': 'merge_sorted', 'input': [[1, 2, 3], [4, 5, 6]], 'expected': [1, 2, 3, 4, 5, 6]},
                    {'function': 'merge_sorted', 'input': [[], [1, 2, 3]], 'expected': [1, 2, 3]},
                    {'function': 'merge_sorted', 'input': [[1, 2, 3], []], 'expected': [1, 2, 3]},
                ])
            }
        ]
        
        for challenge in challenges:
            cursor.execute('''
                INSERT INTO challenges (title, description, difficulty, starter_code, test_cases)
                VALUES (?, ?, ?, ?, ?)
            ''', (challenge['title'], challenge['description'], challenge['difficulty'],
                  challenge['starter_code'], challenge['test_cases']))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

if __name__ == '__main__':
    init_database()
