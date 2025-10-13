# Data Management Guide

## Overview
All seed data is now organized in JSON files within the `data/` folder for easy management and scalability.

## Folder Structure

```
data/
├── challenges/          # Coding challenges
│   ├── 01-sum-of-two-numbers.json
│   ├── 02-reverse-string.json
│   ├── 03-find-maximum.json
│   ├── 04-check-palindrome.json
│   ├── 05-fibonacci-sequence.json
│   ├── 06-two-sum.json
│   ├── 07-valid-parentheses.json
│   └── 08-merge-sorted-arrays.json
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
  "order": 1,
  "estimated_hours": 3
}
```

### Lesson Format
```json
{
  "module_id": 1,
  "title": "Lesson Title",
  "order": 1,
  "estimated_minutes": 15,
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
5. Create the database records with proper relationships

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

**Last Updated**: October 13, 2025
**Data Files**: 8 challenges, 10 achievements, 4 modules, 7 lessons
