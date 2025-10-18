# Data Management Guide

## Overview
All seed data is now organized in JSON files within the `data/` folder for easy management and scalability.

## Folder Structure

```
data/
├── challenges/          # Coding challenges (67 total)
│   ├── 01-08: Original challenges
│   ├── 09-12: Output & Variables
│   ├── 13-15: Data Types, Numbers & Casting
│   ├── 16-20: Strings
│   ├── 21-23: Booleans & Operators
│   ├── 24-28: Lists
│   ├── 29-31: Tuples
│   ├── 32-34: Sets
│   ├── 35-38: Dictionaries
│   ├── 39-43: Control Flow
│   ├── 44-48: Functions
│   ├── 49-52: OOP
│   ├── 53-55: Modules, JSON & RegEx
│   ├── 56-58: Error Handling & Files
│   ├── 59-62: Data Structures
│   └── 63-67: Algorithms
│
├── achievements/        # User achievements
│   ├── 01-first-blood.json
│   ├── 02-winning-streak.json
│   ├── 03-perfect-game.json
│   ├── 04-speed-demon.json
│   ├── 05-veteran.json
│   ├── 06-master-coder.json
│   ├── 07-challenge-accepted.json
│   ├── 08-social-butterfly.json
│   ├── 09-comeback-king.json
│   └── 10-no-mercy.json
│
├── modules/             # Learning modules
│   ├── 01-python-basics.json
│   ├── 02-control-flow.json
│   ├── 03-data-structures.json
│   └── 04-functions.json
│
└── lessons/             # Lessons organized by module
    ├── 01-python-basics/
    │   ├── 01-hello-world.json
    │   ├── 02-variables.json
    │   └── 03-basic-math.json
    ├── 02-control-flow/
    │   ├── 01-if-statements.json
    │   └── 02-for-loops.json
    ├── 03-data-structures/
    │   └── 01-lists.json
    └── 04-functions/
        └── 01-defining-functions.json
```

## JSON File Formats

### Challenge Format
```json
{
  "title": "Challenge Title",
  "description": "Detailed description",
  "difficulty": "Easy|Medium|Hard",
  "starter_code": "def function_name():\n    pass",
  "test_cases": [
    {"input": [args], "expected": result}
  ],
  "time_limit": 300
}
```

### Achievement Format
```json
{
  "name": "Achievement Name",
  "description": "Achievement description",
  "icon": "bi-icon-name",
  "points": 10,
  "criteria": {
    "type": "wins|win_streak|etc",
    "value": 1
  }
}
```

### Module Format
```json
{
  "title": "Module Title",
  "description": "Module description",
  "icon": "bi-icon-name",
  "difficulty": "Beginner|Intermediate|Advanced",
  "order": 1
}
```

**Note**: The `estimated_hours` field is automatically calculated as the sum of all lesson times within the module, converted to hours (rounded to 1 decimal place).

### Lesson Format
```json
{
  "module_id": 1,
  "title": "Lesson Title",
  "order": 1,
  "reading_content": "<h3>HTML content here</h3>",
  "starter_code": "# Starting code",
  "solution_code": "# Solution code",
  "learning_objectives": ["Objective 1", "Objective 2"],
  "key_concepts": ["Concept 1", "Concept 2"],
  "test_cases": [
    {
      "name": "Test 1",
      "input": "",
      "expected_output": "result"
    }
  ],
  "hints": ["Hint 1", "Hint 2"],
  "visual_content": {}
}
```

**Note**: The `estimated_minutes` field is automatically calculated based on:
- **Word count** in reading_content (200 words/minute reading speed)
- **Code lines** in starter_code and solution_code (3 lines/minute code reading speed)
- **Base practice time** (5 minutes minimum)
- Result is rounded to nearest 5 minutes (min: 5, max: 60)

## How to Use

### Adding New Content

#### 1. Add a Challenge
Create a new JSON file in `data/challenges/` with the next number:
```bash
# Example: data/challenges/09-new-challenge.json
```

#### 2. Add an Achievement
Create a new JSON file in `data/achievements/`:
```bash
# Example: data/achievements/11-new-achievement.json
```

#### 3. Add a Module
1. Create the module JSON in `data/modules/`:
   ```bash
   # Example: data/modules/05-new-module.json
   ```
2. Create a folder for its lessons:
   ```bash
   mkdir data/lessons/05-new-module
   ```

#### 4. Add a Lesson
Create a JSON file in the appropriate lesson folder:
```bash
# Example: data/lessons/01-python-basics/04-new-lesson.json
```

### Seeding the Database

After adding or modifying JSON files, run:

```bash
python seed_data.py
```

This will:
1. Load all challenges from `data/challenges/*.json`
2. Load all achievements from `data/achievements/*.json`
3. Load all modules from `data/modules/*.json`
4. Load all lessons from `data/lessons/**/*.json`
5. **Automatically calculate** estimated reading time for each lesson based on content
6. Create the database records with proper relationships

### Automatic Time Calculation

The seeding script automatically calculates all time estimates:

#### Lesson Reading Time (`estimated_minutes`)
The `calculate_reading_time()` function analyzes each lesson:

- **Analyzes reading_content**: Strips HTML tags and counts words
- **Analyzes code content**: Counts non-empty, non-comment lines
- **Calculates time**:
  - Text reading: 200 words/minute (average adult reading speed)
  - Code reading: 3 lines/minute (slower due to comprehension)
  - Base practice time: +5 minutes for hands-on exercises
- **Rounds intelligently**: Result rounded to nearest 5 minutes
- **Enforces bounds**: Minimum 5 minutes, maximum 60 minutes

**You don't need to specify `estimated_minutes`** in lesson JSON files!

#### Module Study Time (`estimated_hours`)
After all lessons are created, the script:

1. Sums up all `estimated_minutes` from lessons in each module
2. Converts to hours (divides by 60)
3. Rounds to 1 decimal place for display

**You don't need to specify `estimated_hours`** in module JSON files!

**Example Output:**
```
Creating lessons from 4 folders...
    ✓ Hello World & Print Function (5 min)
    ✓ Variables and Data Types (10 min)
    ✓ Basic Math Operations (10 min)

Calculating module estimated hours...
  ✓ Python Basics: 25 min = 0.4 hours
```

## Important Notes

### Module and Lesson Relationships
- The `order` field in module JSON determines the module number
- Lesson folders use the format `01-module-name` where `01` matches the module order
- The script automatically maps lesson `module_id` based on folder naming

### Naming Conventions
- Use kebab-case for filenames: `01-my-lesson.json`
- Start with a number for ordering: `01-`, `02-`, etc.
- Module folders must match the module order number

### Foreign Key Constraints
The seeding script handles foreign keys by:
1. Deleting lesson progress records first
2. Then deleting lessons
3. Then deleting modules
4. Finally creating new records

### JSON Validation
Ensure your JSON files are valid:
- Use proper quotes (double quotes for JSON)
- Escape special characters in strings
- Use `true`/`false` (lowercase) for booleans
- No trailing commas

## Troubleshooting

### Error: "Cannot delete or update a parent row"
- The database has existing records with foreign key relationships
- Run `python seed_data.py` again - it now handles this automatically

### Error: "JSON decode error"
- Check your JSON file syntax
- Use a JSON validator: https://jsonlint.com/

### Error: "No such file or directory"
- Ensure all folders exist in the `data/` directory
- Check folder naming matches module order numbers

## Benefits of JSON-Based Data Management

✅ **Easy Editing**: Edit content without touching Python code
✅ **Version Control**: Better Git diffs for content changes
✅ **Scalability**: Easy to add hundreds of lessons
✅ **Collaboration**: Multiple people can add content simultaneously
✅ **Validation**: JSON schema validation possible
✅ **Export/Import**: Easy to backup or migrate data
✅ **Non-Technical**: Content creators don't need Python knowledge

## Next Steps

1. Add more lessons to existing modules
2. Create new advanced modules (OOP, File I/O, etc.)
3. Add more challenges across all difficulty levels
4. Create achievement badges and graphics
5. Implement JSON schema validation
6. Add content localization support

---

**Last Updated**: October 18, 2025
**Data Files**: 67 challenges, 10 achievements, 7 modules, 41 lessons
