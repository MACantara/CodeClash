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
└── └── 63-67: Algorithms
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



**Note**: The `estimated_hours` field is automatically calculated as the sum of all lesson times within the module, converted to hours (rounded to 1 decimal place).

## How to Use

### Adding New Content

#### 1. Add a Challenge
Create a new JSON file in `data/challenges/` with the next number:
```bash
# Example: data/challenges/09-new-challenge.json
```

## Troubleshooting

### Error: "JSON decode error"
- Check your JSON file syntax
- Use a JSON validator: https://jsonlint.com/

### Error: "No such file or directory"
- Ensure all folders exist in the `data/` directory
- Check folder naming matches module order numbers

## Benefits of JSON-Based Data Management

✅ **Easy Editing**: Edit content without touching Python code
✅ **Version Control**: Better Git diffs for content changes
✅ **Scalability**: Easy to add hundreds of content
✅ **Collaboration**: Multiple people can add content simultaneously
✅ **Validation**: JSON schema validation possible
✅ **Export/Import**: Easy to backup or migrate data
✅ **Non-Technical**: Content creators don't need Python knowledge

---

**Last Updated**: October 24, 2025
**Data Files**: 67 challenges
