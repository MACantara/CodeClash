# CodeClash - Python Practice Platform# CodeClash - Python Practice Platform# CodeClash - 1v1 Python Tournament Platform



A Flask-based web application for practicing Python coding challenges with instant feedback.



## FeaturesA Flask-based web application for practicing Python coding challenges with instant feedback.A Flask-based web application for competitive 1v1 Python programming tournaments with real-time leaderboards.



- **Practice Mode**: Solve Python challenges at your own pace

- **Instant Feedback**: Automatic code testing with detailed results

- **Multiple Challenges**: Various Python problems from Easy to Hard difficulty## Features## Features

- **Time Tracking**: Track your solving time for each challenge

- **Live Code Editor**: Write and test your solutions in the browser

- **Error Detection**: Get immediate feedback on code errors

- **Practice Mode**: Solve Python challenges at your own pace- **Matchmaking Lobby System**: Find opponents through various matchmaking options

## Technologies Used

- **Instant Feedback**: Automatic code testing with detailed results- **Quick Match**: Get instantly matched with available players

- **Backend**: Python 3, Flask

- **Database**: SQLite (SQLAlchemy ORM)- **Multiple Challenges**: Various Python problems from Easy to Hard difficulty- **Difficulty-Based Matching**: Choose to match with players on specific difficulty levels

- **Frontend**: HTML5, Tailwind CSS, JavaScript

- **Code Editor**: Ace Editor- **Time Tracking**: Track your solving time for each challenge- **Custom Lobby Rooms**: Create your own rooms and wait for challengers

- **Icons**: Bootstrap Icons

- **Live Code Editor**: Write and test your solutions in the browser- **Public/Private Lobbies**: Control room visibility

## Installation

- **Error Detection**: Get immediate feedback on code errors- **Real-time Lobby Updates**: See available rooms and player counts in real-time

1. Clone the repository:

```bash- **1v1 Tournament System**: Challenge other developers to coding duels

git clone <repository-url>

cd CodeClash## Technologies Used- **Real-time Scoring**: Automatic code testing with instant feedback

```

- **Victory Conditions**: Win by solving problems with fewer errors and faster time

2. Create a virtual environment (optional but recommended):

```bash- **Backend**: Python 3, Flask- **Global Leaderboard**: Track your progress and compete for the top spot

python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate- **Database**: SQLite (SQLAlchemy ORM)- **Rating System**: Earn or lose rating points based on match outcomes

```

- **Frontend**: HTML5, Tailwind CSS, JavaScript- **Multiple Challenges**: Various Python problems from Easy to Hard difficulty

3. Install dependencies:

```bash- **Code Editor**: Ace Editor- **Live Code Editor**: Write and test your solutions in the browser

pip install -r requirements.txt

```- **Icons**: Bootstrap Icons



4. Initialize the database:## Technologies Used

```bash

python init_db.py## Installation

```

- **Backend**: Python 3, Flask

5. (Optional) Seed with sample challenges:

```bash1. Clone the repository:- **Database**: SQLite

python seed_data.py

``````bash- **Frontend**: HTML5, Tailwind CSS, JavaScript



6. Run the application:git clone <repository-url>- **Icons**: Bootstrap Icons

```bash

python app.pycd CodeClash

```

```## Installation

7. Open your browser and navigate to:

```

http://localhost:5000

```2. Create a virtual environment (optional but recommended):1. Clone the repository:



## How to Use```bash```bash



1. **Start Practice**: Click "Practice Mode" on the home pagepython -m venv venvgit clone <repository-url>

2. **Get Random Challenge**: A random challenge will be selected for you

3. **Write Your Code**: Use the built-in code editor to write your solutionsource venv/bin/activate  # On Windows: venv\Scripts\activatecd IT-Olympics-Python-Programming

4. **Test Your Code**: Click "Run Tests" to check if your solution works

5. **Submit Solution**: Once satisfied, click "Submit" to finalize``````

6. **View Results**: See your completion time and error count



## Project Structure

3. Install dependencies:2. Create a virtual environment (optional but recommended):

```

CodeClash/```bash```bash

├── app.py                  # Main Flask application entry point

├── config.py              # Application configuration and factorypip install -r requirements.txtpython -m venv venv

├── init_db.py             # Database initialization script

├── seed_data.py           # Load challenges from JSON files```source venv/bin/activate  # On Windows: venv\Scripts\activate

├── requirements.txt       # Python dependencies

├── README.md              # This file```

├── models/                # Database models

│   ├── __init__.py       # Models package initialization4. Initialize the database:

│   ├── challenge.py      # Challenge model

│   └── match.py          # Match (practice session) model```bash3. Install dependencies:

├── routes/                # Application routes

│   ├── __init__.py       # Routes registrationpython init_db.py```bash

│   ├── challenges.py     # Challenge endpoints

│   ├── matches.py        # Match/practice endpoints```pip install -r requirements.txt

│   └── pages.py          # Page rendering routes

├── utils/                 # Utility functions```

│   ├── __init__.py       # Utils package initialization

│   └── code_testing.py   # Code execution and testing5. (Optional) Seed with sample challenges:

├── templates/             # HTML templates

│   ├── base.html         # Base layout with navigation```bash4. Initialize the database:

│   ├── index.html        # Home page

│   └── match.html        # Challenge/coding arenapython seed_data.py```bash

├── static/               # Static assets

│   ├── css/```python database.py

│   │   └── style.css     # Custom styles and animations

│   └── js/```

└── data/                 # Challenge data

    └── challenges/       # JSON files with coding challenges6. Run the application:

```

```bash5. Run the application:

## Challenges Included

python app.py```bash

The platform includes 50+ Python challenges covering various topics:

- Basic syntax and operations```python app.py

- String manipulation

- List and tuple operations```

- Set and dictionary operations

- Control flow (if/else, loops)7. Open your browser and navigate to:

- Functions and lambdas

- Recursion and generators```6. Open your browser and navigate to:

- Object-oriented programming

- File operations and regexhttp://localhost:5000```

- And many more!

```http://localhost:5000

Each challenge includes:

- Problem description```

- Example test cases

- Starter code template## How to Use

- Automated test cases for validation

- Difficulty rating (Easy, Medium, Hard)## How to Play



## Adding New Challenges1. **Start Practice**: Click "Practice Mode" on the home page



To add new challenges, create JSON files in the `data/challenges/` directory following this format:2. **Get Random Challenge**: A random challenge will be selected for you### Method 1: Quick Match (Recommended for Beginners)



```json3. **Write Your Code**: Use the built-in code editor to write your solution1. **Register/Login**: Create an account or login with an existing username

{

  "id": 1,4. **Test Your Code**: Click "Run Tests" to check if your solution works2. **Enter Lobby**: Click "Enter Lobby" from the home page

  "title": "Challenge Title",

  "description": "Problem description with examples...",5. **Submit Solution**: Once satisfied, click "Submit" to finalize3. **Quick Match**: Click the green "Quick Match" button or choose a specific difficulty

  "difficulty": "Easy",

  "starter_code": "def solution():\n    # Write your code here\n    pass",6. **View Results**: See your completion time and error count4. **Auto-Match**: System will either match you with an existing lobby or create one for you

  "test_cases": [

    {5. **Wait**: Wait for an opponent to join (usually takes seconds)

      "input": "input_value",

      "expected": "expected_output",## Project Structure6. **Battle**: Once matched, you'll be redirected to the coding arena

      "description": "Test case description"

    }7. **Code Your Solution**: Write Python code to solve the problem

  ],

  "time_limit": 300```8. **Submit**: Submit your solution when ready

}

```CodeClash/9. **Win**: The player with fewer errors wins; if tied, fastest time wins!



Then run `python seed_data.py` to load them into the database.├── app.py                  # Main Flask application entry point



## Database Schema├── config.py              # Application configuration and factory### Method 2: Create Custom Room



### Challenge├── init_db.py             # Database initialization script1. **Register/Login**: Create an account or login with an existing username

- `id`: Primary key

- `title`: Challenge name├── seed_data.py           # Load challenges and achievements2. **Enter Lobby**: Navigate to the Lobby page

- `description`: Problem description

- `difficulty`: Easy, Medium, or Hard├── requirements.txt       # Python dependencies3. **Create Room**: Click "Create Room" and configure your preferences

- `starter_code`: Initial code template

- `test_cases`: JSON array of test cases├── README.md              # This file4. **Wait**: Wait for another player to join your room

- `time_limit`: Suggested time limit in seconds

├── models/                # Database models5. **Start Match**: Match begins automatically when room is full

### Match

- `id`: Primary key│   ├── __init__.py       # Models package initialization

- `challenge_id`: Foreign key to Challenge

- `status`: Match status (active, completed)│   ├── challenge.py      # Challenge model### Method 3: Join Existing Room

- `player_code`: Submitted solution code

- `player_errors`: Number of test failures│   └── match.py          # Match (practice session) model1. **Register/Login**: Create an account or login with an existing username

- `player_time`: Time taken to complete (seconds)

- `player_submitted`: Whether solution was submitted├── routes/                # Application routes2. **Enter Lobby**: Navigate to the Lobby page

- `started_at`: Match start timestamp

- `ended_at`: Match end timestamp│   ├── __init__.py       # Routes registration3. **Browse Rooms**: See all available public lobbies



## API Endpoints│   ├── challenges.py     # Challenge endpoints4. **Join**: Click "Join" on any room you'd like to enter



### Challenges│   ├── matches.py        # Match/practice endpoints5. **Start Match**: Match begins immediately or when room fills up

- `GET /challenges` - List all challenges

│   └── pages.py          # Page rendering routes

### Matches

- `POST /match/create` - Create a new practice session├── utils/                 # Utility functions## Project Structure

- `GET /match/<id>` - View match page

- `POST /match/<id>/run` - Test code without submitting│   ├── __init__.py       # Utils package initialization

- `POST /match/<id>/submit` - Submit solution

- `GET /match/<id>/status` - Get match status│   └── code_testing.py   # Code execution and testing```



### Pages├── templates/             # HTML templatesIT-Olympics-Python-Programming/

- `GET /` - Home page

│   ├── base.html         # Base layout with navigation├── app.py                  # Main Flask application with all routes

## Future Enhancements

│   ├── index.html        # Home page├── database.py             # Database initialization and schema

- Challenge categories and filtering

- Progress tracking and statistics│   └── match.html        # Challenge/coding arena├── requirements.txt        # Python dependencies

- Multiple programming languages support

- Difficulty-based challenge selection├── static/               # Static assets├── README.md              # This file

- Hint system for challenges

- Code snippets and examples│   ├── css/├── .gitignore             # Git ignore rules

- Challenge search functionality

- User accounts (optional)│   │   └── style.css     # Custom styles and animations├── codeclash.db           # SQLite database (created on first run)



## License│   └── js/├── templates/             # HTML templates



See LICENSE file for details.└── data/                 # Challenge and achievement data│   ├── base.html         # Base layout with navigation



## Contributing    ├── challenges/       # JSON files with coding challenges│   ├── index.html        # Home/Login/Register page



Contributions are welcome! Please feel free to submit a Pull Request.    └── achievements/     # JSON files with achievement definitions│   ├── lobby.html        # Matchmaking lobby (NEW!)



## Notes```│   ├── tournament.html   # Tournament lobby (deprecated)



This is a simplified version of CodeClash focused on solo practice. The following features have been removed:│   ├── match.html        # Match/coding arena

- User authentication and login system

- Matchmaking and lobby system## Challenges Included│   └── leaderboard.html  # Global leaderboard

- 1v1 PvP battles

- Leaderboards and rankings└── static/               # Static assets

- Rating system

- User profiles and statisticsThe platform includes 50+ Python challenges covering various topics:    ├── css/

- Achievement system

- Basic syntax and operations    │   └── style.css     # Custom styles and animations

The application now focuses purely on practicing Python challenges without any competitive or multiplayer features.

- String manipulation    └── js/

- List and tuple operations        └── main.js       # JavaScript utilities

- Set and dictionary operations```

- Control flow (if/else, loops)

- Functions and lambdas## Challenges Included

- Recursion and generators

- And many more!1. **Sum of Two Numbers** (Easy)

2. **Reverse a String** (Easy)

Each challenge includes:3. **Find Maximum** (Easy)

- Problem description4. **Palindrome Checker** (Medium)

- Example test cases5. **Fibonacci Number** (Medium)

- Starter code template6. **Two Sum** (Medium)

- Automated test cases for validation7. **Valid Parentheses** (Hard)

8. **Merge Sorted Arrays** (Hard)

## Adding New Challenges

## Rating System

To add new challenges, create JSON files in the `data/challenges/` directory following this format:

- Start with 1000 rating points

```json- Win: +25 points

{- Loss: -10 points

  "id": 1,- Matches won by fewest errors, then fastest time

  "title": "Challenge Title",

  "description": "Problem description...",## Matchmaking System

  "difficulty": "Easy",

  "starter_code": "def solution():\n    pass",### How Matchmaking Works

  "test_cases": [

    {1. **Quick Match**: Automatically finds or creates a lobby based on availability

      "input": "input_value",2. **Difficulty Filter**: Optional filtering by Easy/Medium/Hard challenges

      "expected": "expected_output",3. **Lobby System**: Players wait in lobbies until match capacity is reached (2 players)

      "description": "Test case description"4. **Auto-Start**: Match automatically starts when lobby is full

    }5. **Real-time Updates**: Lobby list updates every 5 seconds, player status every 2 seconds

  ],

  "time_limit": 300### Lobby Features

}

```- **Public Lobbies**: Visible to all players in the lobby browser

- **Private Lobbies**: Only accessible via direct invitation (future feature)

Then run `python seed_data.py` to load them into the database.- **Room Naming**: Custom names for personal lobbies

- **Challenge Selection**: Host chooses the coding challenge

## Future Enhancements- **Player Count Display**: See current players vs. max capacity

- **Leave Anytime**: Players can leave lobbies before match starts

- Challenge categories and filtering

- Progress tracking and statistics## Future Enhancements

- User accounts (optional)

- More programming languages support- [x] Matchmaking lobby system

- Difficulty-based challenge selection- [x] Quick match feature

- Hint system for challenges- [x] Real-time multiplayer with WebSockets

- [x] Tournament brackets with elimination rounds

## License- [ ] Practice mode (solve challenges without competing)

- [ ] More programming languages (JavaScript, Java, C++)

See LICENSE file for details.- [ ] Code replay feature

- [ ] Friend system and invitations

## Contributing- [ ] Chat functionality in lobbies

- [ ] Spectator mode

Contributions are welcome! Please feel free to submit a Pull Request.- [x] Match history and statistics

- [x] Achievements and badges

## License

This project is open source and available for educational purposes.

## Contributors

Created for IT Olympics Python Programming Competition
