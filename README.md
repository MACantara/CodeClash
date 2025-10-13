# CodeClash - 1v1 Python Tournament Platform

A Flask-based web application for competitive 1v1 Python programming tournaments with real-time leaderboards.

## Features

- **Matchmaking Lobby System**: Find opponents through various matchmaking options
- **Quick Match**: Get instantly matched with available players
- **Difficulty-Based Matching**: Choose to match with players on specific difficulty levels
- **Custom Lobby Rooms**: Create your own rooms and wait for challengers
- **Public/Private Lobbies**: Control room visibility
- **Real-time Lobby Updates**: See available rooms and player counts in real-time
- **1v1 Tournament System**: Challenge other developers to coding duels
- **Real-time Scoring**: Automatic code testing with instant feedback
- **Victory Conditions**: Win by solving problems with fewer errors and faster time
- **Global Leaderboard**: Track your progress and compete for the top spot
- **Rating System**: Earn or lose rating points based on match outcomes
- **Multiple Challenges**: Various Python problems from Easy to Hard difficulty
- **Live Code Editor**: Write and test your solutions in the browser

## Technologies Used

- **Backend**: Python 3, Flask
- **Database**: SQLite
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Icons**: Bootstrap Icons

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd IT-Olympics-Python-Programming
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
python database.py
```

5. Run the application:
```bash
python app.py
```

6. Open your browser and navigate to:
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
IT-Olympics-Python-Programming/
├── app.py                  # Main Flask application with all routes
├── database.py             # Database initialization and schema
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── codeclash.db           # SQLite database (created on first run)
├── templates/             # HTML templates
│   ├── base.html         # Base layout with navigation
│   ├── index.html        # Home/Login/Register page
│   ├── lobby.html        # Matchmaking lobby (NEW!)
│   ├── tournament.html   # Tournament lobby (deprecated)
│   ├── match.html        # Match/coding arena
│   └── leaderboard.html  # Global leaderboard
└── static/               # Static assets
    ├── css/
    │   └── style.css     # Custom styles and animations
    └── js/
        └── main.js       # JavaScript utilities
```

## Challenges Included

1. **Sum of Two Numbers** (Easy)
2. **Reverse a String** (Easy)
3. **Find Maximum** (Easy)
4. **Palindrome Checker** (Medium)
5. **Fibonacci Number** (Medium)
6. **Two Sum** (Medium)
7. **Valid Parentheses** (Hard)
8. **Merge Sorted Arrays** (Hard)

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

## Future Enhancements

- ✅ ~~Matchmaking lobby system~~ (IMPLEMENTED!)
- ✅ ~~Quick match feature~~ (IMPLEMENTED!)
- Real-time multiplayer with WebSockets
- Tournament brackets with elimination rounds
- Practice mode (solve challenges without competing)
- More programming languages (JavaScript, Java, C++)
- Code replay feature
- Friend system and invitations
- Chat functionality in lobbies
- Spectator mode
- Match history and statistics
- Achievements and badges

## License

This project is open source and available for educational purposes.

## Contributors

Created for IT Olympics Python Programming Competition
