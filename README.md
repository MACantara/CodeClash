# CodeClash - 1v1 Python Tournament Platform

A Flask-based web application for competitive 1v1 Python programming tournaments with real-time leaderboards and a practice mode for solo challenges.

## Features

- **Practice Mode**: Solve Python challenges at your own pace
- **Instant Feedback**: Automatic code testing with detailed results
- **Multiple Challenges**: 50+ Python problems from Easy to Hard difficulty
- **Time Tracking**: Track your solving time for each challenge
- **Live Code Editor**: Write and test your solutions in the browser with Ace Editor
- **Error Detection**: Get immediate feedback on code errors
- **Matchmaking Lobby System**: Find opponents through various matchmaking options
- **Quick Match**: Get instantly matched with available players or create custom rooms
- **Difficulty-Based Matching**: Choose to match with players on specific difficulty levels
- **Custom Lobby Rooms**: Create your own rooms and wait for challengers
- **Public/Private Lobbies**: Control room visibility
- **Real-time Lobby Updates**: See available rooms and player counts in real-time
- **1v1 Tournament System**: Challenge other developers to coding duels
- **Real-time Scoring**: Automatic code testing with instant feedback
- **Victory Conditions**: Win by solving problems with fewer errors and faster time
- **Global Leaderboard**: Track your progress and compete for the top spot
- **Rating System**: Earn or lose rating points based on match outcomes

## Technologies Used

- **Backend**: Python 3, Flask
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Code Editor**: Ace Editor
- **Icons**: Bootstrap Icons

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd CodeClash
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. (Optional) Seed with sample challenges and achievements:
```bash
python seed_data.py
```

6. Run the application:
```bash
python app.py
```

7. Open your browser and navigate to:
```
http://localhost:5000
```

## How to Play

### Method 1: Quick Match (Recommended for Beginners)

1. **Register/Login**: Create an account or login with an existing username
2. **Enter Lobby**: Click "Enter Lobby" from the home page
3. **Quick Match**: Click the green "Quick Match" button or choose a specific difficulty
4. **Auto-Match**: System will either match you with an existing lobby or create one for you
5. **Wait**: Wait for an opponent to join (usually takes seconds)
6. **Battle**: Once matched, you'll be redirected to the coding arena
7. **Code Your Solution**: Write Python code to solve the problem
8. **Submit**: Submit your solution when ready
9. **Win**: The player with fewer errors wins; if tied, fastest time wins!

### Method 2: Create Custom Room

1. **Register/Login**: Create an account or login with an existing username
2. **Enter Lobby**: Navigate to the Lobby page
3. **Create Room**: Click "Create Room" and configure your preferences
4. **Wait**: Wait for another player to join your room
5. **Start Match**: Match begins automatically when room is full

### Method 3: Join Existing Room

1. **Register/Login**: Create an account or login with an existing username
2. **Enter Lobby**: Navigate to the Lobby page
3. **Browse Rooms**: See all available public lobbies
4. **Join**: Click "Join" on any room you'd like to enter
5. **Start Match**: Match begins immediately or when room fills up

## Project Structure

```
CodeClash/
├── app.py                  # Main Flask application entry point
├── config.py              # Application configuration and factory
├── database.py            # Database initialization and schema
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── models/                # Database models
│   ├── __init__.py
│   ├── challenge.py       # Challenge model
│   └── match.py           # Match (practice session) model
├── routes/                # Application routes
│   ├── __init__.py        # Routes registration
│   ├── challenges.py      # Challenge endpoints
│   ├── matches.py         # Match/practice endpoints
│   └── pages.py           # Page rendering routes
├── utils/                 # Utility functions
│   ├── __init__.py
│   └── code_testing.py    # Code execution and testing
├── templates/             # HTML templates
│   ├── base.html          # Base layout with navigation
│   ├── index.html         # Home/Login/Register page
│   ├── lobby.html         # Matchmaking lobby
│   ├── match.html         # Match/coding arena
│   └── leaderboard.html   # Global leaderboard
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Custom styles and animations
│   └── js/
│       └── main.js        # JavaScript utilities
└── data/                  # Challenge and achievement data
    ├── challenges/        # JSON files with coding challenges
    └── achievements/      # JSON files with achievement definitions
```

## Challenges Included

The platform includes 50+ Python challenges covering various topics:

- **Basic Syntax**: Sum of two numbers, reverse string, find maximum
- **String Operations**: Palindrome checker, string slicing, string modification, string formatting
- **Collections**: List operations, list comprehension, tuples, sets, dictionaries
- **Control Flow**: If/else, while loops, for loops, nested loops, FizzBuzz
- **Functions**: Function arguments, *args/**kwargs, lambda functions, recursion
- **Advanced**: Generators, classes, inheritance, polymorphism, iterators
- **Data Structures**: Stack, queue, binary tree, hash table
- **Algorithms**: Linear search, sorting, two-sum problem, valid parentheses, merge sorted arrays
- **Utilities**: JSON parsing, regex matching, math operations, file operations, exception handling

Sample challenges:

1. **Sum of Two Numbers** (Easy)
2. **Reverse a String** (Easy)
3. **Find Maximum** (Easy)
4. **Palindrome Checker** (Medium)
5. **Fibonacci Number** (Medium)
6. **Two Sum** (Medium)
7. **Valid Parentheses** (Hard)
8. **Merge Sorted Arrays** (Hard)

Each challenge includes:
- Problem description with examples
- Starter code template
- Automated test cases for validation
- Difficulty rating (Easy, Medium, Hard)

## Database Schema

### Challenge
- `id`: Primary key
- `title`: Challenge name
- `description`: Problem description
- `difficulty`: Easy, Medium, or Hard
- `starter_code`: Initial code template
- `test_cases`: JSON array of test cases
- `time_limit`: Suggested time limit in seconds

### Match
- `id`: Primary key
- `challenge_id`: Foreign key to Challenge
- `status`: Match status (active, completed)
- `player_code`: Submitted solution code
- `player_errors`: Number of test failures
- `player_time`: Time taken to complete (seconds)
- `player_submitted`: Whether solution was submitted
- `started_at`: Match start timestamp
- `ended_at`: Match end timestamp

## API Endpoints

### Challenges
- `GET /challenges` - List all available challenges
- `GET /api/challenges/data` - Get all challenges data for IndexedDB

### Matches
- `POST /match/create` - Create a new practice session
- `GET /match/<id>` - View match page
- `GET /match/<id>/status` - Get match status

### Pages
- `GET /` - Home page

## Rating System

- Start with 1000 rating points
- Win: +25 points
- Loss: -10 points
- Matches won by fewest errors, then fastest time

## Matchmaking System

### How Matchmaking Works

1. **Quick Match**: Automatically finds or creates a lobby based on availability
2. **Difficulty Filter**: Optional filtering by Easy/Medium/Hard challenges
3. **Lobby System**: Players wait in lobbies until match capacity is reached (2 players)
4. **Auto-Start**: Match automatically starts when lobby is full
5. **Real-time Updates**: Lobby list updates every 5 seconds, player status every 2 seconds

### Lobby Features

- **Public Lobbies**: Visible to all players in the lobby browser
- **Private Lobbies**: Only accessible via direct invitation (future feature)
- **Room Naming**: Custom names for personal lobbies
- **Challenge Selection**: Host chooses the coding challenge
- **Player Count Display**: See current players vs. max capacity
- **Leave Anytime**: Players can leave lobbies before match starts

## Adding New Challenges

To add new challenges, create JSON files in the `data/challenges/` directory following this format:

```json
{
  "id": 1,
  "title": "Challenge Title",
  "description": "Problem description with examples...",
  "difficulty": "Easy",
  "starter_code": "def solution():\n    # Write your code here\n    pass",
  "test_cases": [
    {
      "input": "input_value",
      "expected": "expected_output",
      "description": "Test case description"
    }
  ],
  "time_limit": 300
}
```

Then run `python seed_data.py` to load them into the database.

## Future Enhancements

- [x] Matchmaking lobby system
- [x] Quick match feature
- [x] Real-time multiplayer with WebSockets
- [x] Tournament brackets with elimination rounds
- [x] Match history and statistics
- [x] Achievements and badges
- [ ] Practice mode (solve challenges without competing)
- [ ] More programming languages (JavaScript, Java, C++)
- [ ] Code replay feature
- [ ] Friend system and invitations
- [ ] Chat functionality in lobbies
- [ ] Spectator mode

## License

This project is open source and available for educational purposes.

## Contributors

Created for IT Olympics Python Programming Competition

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
