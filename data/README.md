# CodeClash Data Directory



This directory contains all challenge and achievement data for CodeClash in JSON format.



## Directory StructureThis directory contains all challenge and achievement data for CodeClash in JSON format.## Overview



```All seed data is now organized in JSON files within the `data/` folder for easy management and scalability.

data/

├── challenges/          # Coding challenges (67 total)## Directory Structure

│   ├── 01-08: Original challenges

│   ├── 09-12: Output & Variables## Folder Structure

│   ├── 13-15: Data Types, Numbers & Casting

│   ├── 16-20: Strings- **challenges/**: Contains JSON files for all coding challenges

│   ├── 21-23: Booleans & Operators

│   ├── 24-28: Lists- **achievements/**: Contains JSON files for achievement definitions```

│   ├── 29-31: Tuples

│   ├── 32-34: Setsdata/

│   ├── 35-38: Dictionaries

│   ├── 39-43: Control Flow## Folder Structure├── challenges/          # Coding challenges (67 total)

│   ├── 44-48: Functions

│   ├── 49-52: OOP│   ├── 01-08: Original challenges

│   ├── 53-55: Modules, JSON & RegEx

│   ├── 56-58: Error Handling & Files```│   ├── 09-12: Output & Variables

│   ├── 59-62: Data Structures  

│   └── 63-67: Algorithmsdata/│   ├── 13-15: Data Types, Numbers & Casting

└── achievements/        # Achievement definitions

```├── challenges/          # Coding challenges (67 total)│   ├── 16-20: Strings



## Challenges│   ├── 01-08: Original challenges│   ├── 21-23: Booleans & Operators



Each challenge is stored as a JSON file with a standardized format. Challenges are numbered sequentially (01-67+).│   ├── 09-12: Output & Variables│   ├── 24-28: Lists



### Challenge File Template│   ├── 13-15: Data Types, Numbers & Casting│   ├── 29-31: Tuples



Each challenge JSON file follows this comprehensive template:│   ├── 16-20: Strings│   ├── 32-34: Sets



```json│   ├── 21-23: Booleans & Operators│   ├── 35-38: Dictionaries

{

  "problem_number": 1,│   ├── 24-28: Lists│   ├── 39-43: Control Flow

  "problem_name": "Sum of Two Numbers",

  "difficulty": "foundational",│   ├── 29-31: Tuples│   ├── 44-48: Functions

  "programming_language": "python",

  "description": "Write a function that takes two numbers as input and returns their sum...",│   ├── 32-34: Sets│   ├── 49-52: OOP

  "input_specification": "Two integers or floats separated by a space on a single line...",

  "output_specification": "A single number representing the sum of the two input numbers...",│   ├── 35-38: Dictionaries│   ├── 53-55: Modules, JSON & RegEx

  "sample_inputs": ["2 3", "10 20", "-5 5", "0 0"],

  "sample_outputs": ["5", "30", "0", "0"],│   ├── 39-43: Control Flow│   ├── 56-58: Error Handling & Files

  "explanations": [

    "2 + 3 = 5",│   ├── 44-48: Functions│   ├── 59-62: Data Structures  

    "10 + 20 = 30",

    "-5 + 5 = 0",│   ├── 49-52: OOP└── └── 63-67: Algorithms

    "0 + 0 = 0"

  ],│   ├── 53-55: Modules, JSON & RegEx```

  "notes": [

    "Handle both positive and negative numbers",│   ├── 56-58: Error Handling & Files

    "The function should work with floats as well",

    "Zero plus any number equals that number"│   ├── 59-62: Data Structures  ## JSON File Formats

  ],

  "hints": [└── └── 63-67: Algorithms

    "Use the addition operator (+) in Python",

    "Remember that Python handles both int and float types",```### Challenge Format

    "Consider edge cases like negative numbers and zero"

  ],```json

  "starter_code": "def add_numbers(a, b):\n    # Write your code here\n    pass",

  "test_cases": [## Challenges{

    {"input": [2, 3], "expected": 5},

    {"input": [10, 20], "expected": 30},  "title": "Challenge Title",

    {"input": [-5, 5], "expected": 0},

    {"input": [0, 0], "expected": 0}Each challenge is stored as a JSON file with a standardized format. Challenges are numbered sequentially (01-67+).  "description": "Detailed description",

  ],

  "time_limit": 300  "difficulty": "Easy|Medium|Hard",

}

```### Challenge File Template  "starter_code": "def function_name():\n    pass",



### Field Descriptions  "test_cases": [



| Field | Type | Description |Each challenge JSON file follows this comprehensive template:    {"input": [args], "expected": result}

|-------|------|-------------|

| **problem_number** | Integer | Sequential identifier for the challenge (1-67+) |  ],

| **problem_name** | String | Descriptive name of the challenge |

| **difficulty** | String | Challenge difficulty level: `foundational`, `easy`, `average`, or `difficult` |```json  "time_limit": 300

| **programming_language** | String | Primary language: `python` or `java` |

| **description** | String | Detailed problem statement and requirements |{}

| **input_specification** | String | Format and constraints of input data |

| **output_specification** | String | Format and constraints of expected output |  "problem_number": 1,```

| **sample_inputs** | Array | List of sample input strings for testing |

| **sample_outputs** | Array | Corresponding expected output strings (same length as sample_inputs) |  "problem_name": "Sum of Two Numbers",

| **explanations** | Array | Detailed explanations for each sample (parallel to sample_inputs/outputs) |

| **notes** | Array | Important points, edge cases, and considerations |  "difficulty": "foundational",

| **hints** | Array | Helpful hints to guide the solver without giving away the solution |

| **starter_code** | String | Template code with function signature and comments |  "programming_language": "python",

| **test_cases** | Array | Structured test cases with input/expected output pairs |

| **time_limit** | Integer | Time limit in seconds (typically 300s) |  "description": "Write a function that takes two numbers as input and returns their sum...",**Note**: The `estimated_hours` field is automatically calculated as the sum of all lesson times within the module, converted to hours (rounded to 1 decimal place).



## Achievements  "input_specification": "Two integers or floats separated by a space on a single line...",



Achievement files contain metadata about unlock conditions and reward information. See individual achievement files for details.  "output_specification": "A single number representing the sum of the two input numbers...",## How to Use



## Adding New Challenges  "sample_inputs": ["2 3", "10 20", "-5 5", "0 0"],



When creating a new challenge:  "sample_outputs": ["5", "30", "0", "0"],### Adding New Content



1. Use the naming pattern: `{number:02d}-{slugified-name}.json`  "explanations": [

2. Fill out all required fields from the template above

3. Ensure `sample_inputs` and `sample_outputs` arrays are parallel (same length)    "2 + 3 = 5",#### 1. Add a Challenge

4. Keep `explanations` array aligned with samples

5. Provide at least 2-3 helpful hints    "10 + 20 = 30",Create a new JSON file in `data/challenges/` with the next number:

6. Include diverse test cases covering edge cases

7. Validate JSON syntax using https://jsonlint.com/    "-5 + 5 = 0",```bash



**Example**: `data/challenges/68-prime-checker.json`    "0 + 0 = 0"# Example: data/challenges/09-new-challenge.json



## Troubleshooting  ],```



### Error: "JSON decode error"  "notes": [

- Check your JSON file syntax

- Use a JSON validator: https://jsonlint.com/    "Handle both positive and negative numbers",## Troubleshooting

- Ensure all strings are properly quoted

- Watch for trailing commas in arrays/objects    "The function should work with floats as well",



### Error: "No such file or directory"    "Zero plus any number equals that number"### Error: "JSON decode error"

- Ensure all folders exist in the `data/` directory

- Verify file naming follows the convention: `{number:02d}-{name}.json`  ],- Check your JSON file syntax



## Benefits of JSON-Based Data Management  "hints": [- Use a JSON validator: https://jsonlint.com/



✅ **Easy Editing**: Edit content without touching Python code    "Use the addition operator (+) in Python",

✅ **Version Control**: Better Git diffs for content changes

✅ **Scalability**: Easy to add hundreds of challenges    "Remember that Python handles both int and float types",### Error: "No such file or directory"

✅ **Collaboration**: Multiple people can add content simultaneously

✅ **Validation**: JSON schema validation possible    "Consider edge cases like negative numbers and zero"- Ensure all folders exist in the `data/` directory

✅ **Export/Import**: Easy to backup or migrate data

✅ **Non-Technical**: Content creators don't need programming knowledge  ],- Check folder naming matches module order numbers

✅ **Comprehensive**: Rich metadata for better user experience

  "starter_code": "def add_numbers(a, b):\n    # Write your code here\n    pass",

---

  "test_cases": [## Benefits of JSON-Based Data Management

**Last Updated**: October 24, 2025

**Data Files**: 67 challenges + achievements    {"input": [2, 3], "expected": 5},


    {"input": [10, 20], "expected": 30},✅ **Easy Editing**: Edit content without touching Python code

    {"input": [-5, 5], "expected": 0},✅ **Version Control**: Better Git diffs for content changes

    {"input": [0, 0], "expected": 0}✅ **Scalability**: Easy to add hundreds of content

  ],✅ **Collaboration**: Multiple people can add content simultaneously

  "time_limit": 300✅ **Validation**: JSON schema validation possible

}✅ **Export/Import**: Easy to backup or migrate data

```✅ **Non-Technical**: Content creators don't need Python knowledge



### Field Descriptions---



| Field | Type | Description |**Last Updated**: October 24, 2025

|-------|------|-------------|**Data Files**: 67 challenges

| **problem_number** | Integer | Sequential identifier for the challenge (1-67+) |
| **problem_name** | String | Descriptive name of the challenge |
| **difficulty** | String | Challenge difficulty level: `foundational`, `easy`, `average`, or `difficult` |
| **programming_language** | String | Primary language: `python` or `java` |
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
| **time_limit** | Integer | Time limit in seconds (typically 300s) |

## Achievements

Achievement files contain metadata about unlock conditions and reward information. See individual achievement files for details.

## How to Add New Content

### Adding a New Challenge

Create a new JSON file in `data/challenges/` with the next sequential number:

1. Use the naming pattern: `{number:02d}-{slugified-name}.json`
2. Fill out all required fields from the template above
3. Ensure `sample_inputs` and `sample_outputs` arrays are parallel (same length)
4. Keep `explanations` array aligned with samples
5. Provide at least 2-3 helpful hints
6. Include diverse test cases covering edge cases
7. Validate JSON syntax using https://jsonlint.com/

**Example**: `data/challenges/68-prime-checker.json`

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
✅ **Collaboration**: Multiple people can add content simultaneously
✅ **Validation**: JSON schema validation possible
✅ **Export/Import**: Easy to backup or migrate data
✅ **Non-Technical**: Content creators don't need programming knowledge
✅ **Comprehensive**: Rich metadata for better user experience

---

**Last Updated**: October 24, 2025
**Data Files**: 67 challenges
