# CodeClash - Python Challenge Platform

A Flask-based web application for practicing Python coding challenges with client-side storage using IndexedDB. All data is stored locally in your browser.

## Features

- **Multiple Challenges**: 50+ Python problems from Easy to Hard difficulty
- **Challenge Browsing**: View all available challenges via API
- **Instant Feedback**: Challenges include test cases for validation
- **Live Code Editor**: Write and test your solutions in the browser with Ace Editor
- **Client-Side Storage**: All match and challenge data stored locally in IndexedDB
- **No Code Execution**: Code execution disabled for security
- **Responsive Design**: Built with Tailwind CSS for all screen sizes
- **Challenge Data**: Comprehensive Python coding challenges with descriptions and examples

## Technologies Used

- **Backend**: Python 3, Flask
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Client Storage**: IndexedDB (browser-based)
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

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## How to Use

1. Navigate to `http://localhost:5000` to view the home page
2. Browse available challenges from the challenges endpoint (`/challenges`)
3. View match details at `/match/<match_id>` (data stored in browser's IndexedDB)
4. Challenge data and match information are persisted locally in your browser using IndexedDB

## Project Structure

```
CodeClash/
├── app.py                  # Main Flask application entry point
├── config.py              # Application configuration (no database backend)
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── routes/                # Application routes
│   ├── __init__.py        # Routes registration
│   ├── challenges.py      # Challenge endpoints
│   ├── matches.py         # Match view endpoints
│   └── pages.py           # Page rendering routes
├── templates/             # HTML templates
│   ├── base.html          # Base layout with navigation
│   └── index.html         # Home page
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Custom styles and animations
│   └── js/
│       ├── db.js          # IndexedDB client-side storage
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

## API Endpoints

### Challenges
- `GET /challenges` - List all available challenges as JSON
- `GET /api/challenges/data` - Get all challenges data for IndexedDB synchronization

### Matches
- `POST /match/create` - Create a new match (client-side data stored in IndexedDB)
- `GET /match/<id>` - View match page with IndexedDB-stored data
- `GET /match/<id>/status` - Get match status

### Pages
- `GET /` - Home page

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

The challenges will be automatically loaded from the JSON files in the `data/challenges/` directory when the application starts.

## Future Enhancements

- [ ] User authentication and login system
- [ ] Persistent backend database (SQLite/PostgreSQL)
- [ ] Matchmaking lobby system
- [ ] 1v1 PvP battles
- [ ] Real-time multiplayer with WebSockets
- [ ] Rating system for players
- [ ] Global leaderboard
- [ ] Code execution and automated testing
- [ ] More programming languages (JavaScript, Java, C++)
- [ ] Tournament brackets with elimination rounds
- [ ] Chat functionality in lobbies
- [ ] Spectator mode
- [ ] Friend system and invitations
- [ ] Code replay feature
- [ ] Match history and statistics
- [ ] Achievements and badges

## License

This project is open source and available for educational purposes.

## Contributors

Created for IT Olympics Python Programming Competition

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
