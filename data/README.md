# CodeClash Data Directory

This directory contains all challenge and achievement data for CodeClash in JSON format.

## Overview

All seed data is now organized in JSON files within the `data/` folder for easy management and scalability.

## Directory Structure

```
data/
├── challenges/          # Coding challenges (134 total: 67 Python + 67 Java)
│   ├── python/          # Python challenges (67 total)
│   │   ├── 01-08: Original challenges
│   │   ├── 09-12: Output & Variables
│   │   ├── 13-15: Data Types, Numbers & Casting
│   │   ├── 16-20: Strings
│   │   ├── 21-23: Booleans & Operators
│   │   ├── 24-28: Lists
│   │   ├── 29-31: Tuples
│   │   ├── 32-34: Sets
│   │   ├── 35-38: Dictionaries
│   │   ├── 39-43: Control Flow
│   │   ├── 44-48: Functions
│   │   ├── 49-52: OOP
│   │   ├── 53-55: Modules, JSON & RegEx
│   │   ├── 56-58: Error Handling & Files
│   │   ├── 59-62: Data Structures  
│   │   └── 63-67: Algorithms
│   └── java/            # Java challenges (67 total)
│       ├── 01-08: Original challenges
│       ├── 09-12: Output & Variables
│       ├── 13-15: Data Types, Numbers & Casting
│       ├── 16-20: Strings
│       ├── 21-23: Booleans & Operators
│       ├── 24-28: Arrays & ArrayLists
│       ├── 29-31: Arrays (Advanced)
│       ├── 32-34: Sets
│       ├── 35-38: HashMaps
│       ├── 39-43: Control Flow
│       ├── 44-48: Methods
│       ├── 49-52: OOP
│       ├── 53-55: Libraries & Utilities
│       ├── 56-58: Exception Handling
│       ├── 59-62: Data Structures  
│       └── 63-67: Algorithms
└── achievements/        # Achievement definitions
```

## Challenges

Each challenge is stored as a JSON file with a standardized format. Challenges are numbered sequentially (01-67) and available in both **Python** and **Java**.

### Challenge Organization

- **Python Challenges**: Located in `data/challenges/python/`
  - 67 challenges covering Python fundamentals to advanced algorithms
  - Uses Python-specific syntax, functions, and data structures
  - Starter code includes Python function definitions

- **Java Challenges**: Located in `data/challenges/java/`
  - 67 challenges parallel to Python challenges
  - Uses Java-specific syntax, methods, and data structures
  - Starter code includes Java class and method definitions

Both language tracks cover the same topics and difficulty levels, allowing learners to practice in their preferred language or compare implementations across languages.

### Challenge File Template

Each challenge JSON file follows this comprehensive template:

```json
{
  "problem_number": 1,
  "problem_name": "Sum of Two Numbers",
  "difficulty": "foundational",
  "programming_language": "python",
  "description": "Write a function that takes two numbers as input and returns their sum...",
  "input_specification": "Two integers or floats separated by a space on a single line...",
  "output_specification": "A single number representing the sum of the two input numbers...",
  "sample_inputs": ["2 3", "10 20", "-5 5", "0 0"],
  "sample_outputs": ["5", "30", "0", "0"],
  "explanations": [
    "2 + 3 = 5",
    "10 + 20 = 30",
    "-5 + 5 = 0",
    "0 + 0 = 0"
  ],
  "notes": [
    "Handle both positive and negative numbers",
    "The function should work with floats as well",
    "Zero plus any number equals that number"
  ],
  "hints": [
    "Use the addition operator (+) in Python",
    "Remember that Python handles both int and float types",
    "Consider edge cases like negative numbers and zero"
  ],
  "starter_code": "def add_numbers(a, b):\n    # Write your code here\n    pass",
  "test_cases": [
    {"input": [2, 3], "expected": 5},
    {"input": [10, 20], "expected": 30},
    {"input": [-5, 5], "expected": 0},
    {"input": [0, 0], "expected": 0}
  ]
}
```



### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| **problem_number** | Integer | Sequential identifier for the challenge (1-67) |
| **problem_name** | String | Descriptive name of the challenge |
| **difficulty** | String | Challenge difficulty level: `foundational`, `easy`, `average`, or `difficult` |
| **programming_language** | String | Programming language: `python` or `java` |
| **description** | String | Detailed problem statement and requirements |
| **input_specification** | String | Format and constraints of input data |
| **output_specification** | String | Format and constraints of expected output |
| **sample_inputs** | Array | List of sample input strings for testing |
| **sample_outputs** | Array | Corresponding expected output strings (same length as sample_inputs) |
| **explanations** | Array | Detailed explanations for each sample (parallel to sample_inputs/outputs) |
| **notes** | Array | Important points, edge cases, and considerations |
| **hints** | Array | Helpful hints to guide the solver without giving away the solution |
| **starter_code** | String | Template code with function signature and comments |
| **test_cases** | Array | Structured test cases with input/expected output pairs |

## Achievements

Achievement files contain metadata about unlock conditions and reward information. See individual achievement files for details.

## How to Add New Content

### Adding a New Challenge

Create a new JSON file in `data/challenges/python/` or `data/challenges/java/` with the next sequential number:

1. Use the naming pattern: `{number:02d}-{slugified-name}.json`
2. Fill out all required fields from the template above
3. Ensure `sample_inputs` and `sample_outputs` arrays are parallel (same length)
4. Keep `explanations` array aligned with samples
5. Provide at least 2-3 helpful hints
6. Include diverse test cases covering edge cases
7. Validate JSON syntax using https://jsonlint.com/
8. Use language-appropriate syntax in `starter_code` field:
   - Python: `def function_name(params):`
   - Java: `public static returnType methodName(params)`

**Example Python**: `data/challenges/python/68-prime-checker.json`  
**Example Java**: `data/challenges/java/68-prime-checker.json`

## Troubleshooting

### Error: "JSON decode error"
- Check your JSON file syntax
- Use a JSON validator: https://jsonlint.com/
- Ensure all strings are properly quoted
- Watch for trailing commas in arrays/objects

### Error: "No such file or directory"
- Ensure all folders exist in the `data/` directory
- Verify file naming follows the convention: `{number:02d}-{name}.json`

## Benefits of JSON-Based Data Management

✅ **Easy Editing**: Edit content without touching Python code  
✅ **Version Control**: Better Git diffs for content changes  
✅ **Scalability**: Easy to add hundreds of challenges  
✅ **Multi-Language**: Support both Python and Java with same structure  
✅ **Collaboration**: Multiple people can add content simultaneously  
✅ **Validation**: JSON schema validation possible  
✅ **Export/Import**: Easy to backup or migrate data  
✅ **Non-Technical**: Content creators don't need programming knowledge  
✅ **Comprehensive**: Rich metadata for better user experience  

---

**Last Updated**: October 24, 2025  
**Data Files**: 134 challenges (67 Python + 67 Java)
