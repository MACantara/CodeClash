"""
Database seeding script for CodeClash
Seeds challenges, achievements, and learning modules into the database
"""
from models import db, Challenge, Achievement
from models.learning import Module, Lesson
import json

def seed_challenges():
    """Seed initial challenges"""
    challenges_data = [
        # Easy Challenges
        {
            'title': 'Sum of Two Numbers',
            'description': 'Write a function called `add_numbers(a, b)` that returns the sum of two numbers.',
            'difficulty': 'Easy',
            'starter_code': 'def add_numbers(a, b):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': [2, 3], 'expected': 5},
                {'input': [10, 20], 'expected': 30},
                {'input': [-5, 5], 'expected': 0},
                {'input': [0, 0], 'expected': 0}
            ]),
            'time_limit': 300
        },
        {
            'title': 'Reverse a String',
            'description': 'Write a function called `reverse_string(s)` that returns the reversed version of the input string.',
            'difficulty': 'Easy',
            'starter_code': 'def reverse_string(s):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': ['hello'], 'expected': 'olleh'},
                {'input': ['Python'], 'expected': 'nohtyP'},
                {'input': [''], 'expected': ''},
                {'input': ['a'], 'expected': 'a'}
            ]),
            'time_limit': 300
        },
        {
            'title': 'Find Maximum',
            'description': 'Write a function called `find_max(numbers)` that returns the maximum number in a list.',
            'difficulty': 'Easy',
            'starter_code': 'def find_max(numbers):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': [[1, 5, 3, 9, 2]], 'expected': 9},
                {'input': [[-1, -5, -3]], 'expected': -1},
                {'input': [[42]], 'expected': 42},
                {'input': [[0, 0, 0]], 'expected': 0}
            ]),
            'time_limit': 300
        },
        # Medium Challenges
        {
            'title': 'Check Palindrome',
            'description': 'Write a function called `is_palindrome(s)` that returns True if the string is a palindrome, False otherwise. Ignore case and spaces.',
            'difficulty': 'Medium',
            'starter_code': 'def is_palindrome(s):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': ['racecar'], 'expected': True},
                {'input': ['hello'], 'expected': False},
                {'input': ['A man a plan a canal Panama'], 'expected': True},
                {'input': [''], 'expected': True}
            ]),
            'time_limit': 300
        },
        {
            'title': 'Fibonacci Sequence',
            'description': 'Write a function called `fibonacci(n)` that returns the nth Fibonacci number (0-indexed).',
            'difficulty': 'Medium',
            'starter_code': 'def fibonacci(n):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': [0], 'expected': 0},
                {'input': [1], 'expected': 1},
                {'input': [5], 'expected': 5},
                {'input': [10], 'expected': 55}
            ]),
            'time_limit': 300
        },
        {
            'title': 'Two Sum',
            'description': 'Write a function called `two_sum(nums, target)` that returns indices of two numbers that add up to the target.',
            'difficulty': 'Medium',
            'starter_code': 'def two_sum(nums, target):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': [[2, 7, 11, 15], 9], 'expected': [0, 1]},
                {'input': [[3, 2, 4], 6], 'expected': [1, 2]},
                {'input': [[3, 3], 6], 'expected': [0, 1]}
            ]),
            'time_limit': 300
        },
        # Hard Challenges
        {
            'title': 'Valid Parentheses',
            'description': 'Write a function called `is_valid(s)` that returns True if the parentheses string is valid (properly opened and closed).',
            'difficulty': 'Hard',
            'starter_code': 'def is_valid(s):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': ['()'], 'expected': True},
                {'input': ['()[]{}'], 'expected': True},
                {'input': ['(]'], 'expected': False},
                {'input': ['([)]'], 'expected': False},
                {'input': ['{[]}'], 'expected': True}
            ]),
            'time_limit': 300
        },
        {
            'title': 'Merge Sorted Arrays',
            'description': 'Write a function called `merge_sorted(arr1, arr2)` that merges two sorted arrays into one sorted array.',
            'difficulty': 'Hard',
            'starter_code': 'def merge_sorted(arr1, arr2):\n    # Write your code here\n    pass',
            'test_cases': json.dumps([
                {'input': [[1, 3, 5], [2, 4, 6]], 'expected': [1, 2, 3, 4, 5, 6]},
                {'input': [[1, 2, 3], [4, 5, 6]], 'expected': [1, 2, 3, 4, 5, 6]},
                {'input': [[], [1, 2, 3]], 'expected': [1, 2, 3]},
                {'input': [[1], [2]], 'expected': [1, 2]}
            ]),
            'time_limit': 300
        }
    ]
    
    for challenge_data in challenges_data:
        # Check if challenge already exists
        existing = Challenge.query.filter_by(title=challenge_data['title']).first()
        if not existing:
            challenge = Challenge(**challenge_data)
            db.session.add(challenge)
    
    db.session.commit()
    print(f"Seeded {len(challenges_data)} challenges")

def seed_achievements():
    """Seed achievements"""
    achievements_data = [
        {
            'name': 'First Blood',
            'description': 'Win your first match',
            'icon': 'bi-trophy-fill',
            'points': 10,
            'criteria': json.dumps({'type': 'wins', 'value': 1})
        },
        {
            'name': 'Winning Streak',
            'description': 'Win 5 matches in a row',
            'icon': 'bi-fire',
            'points': 25,
            'criteria': json.dumps({'type': 'win_streak', 'value': 5})
        },
        {
            'name': 'Perfect Game',
            'description': 'Win 3 matches with zero errors',
            'icon': 'bi-star-fill',
            'points': 30,
            'criteria': json.dumps({'type': 'perfect_matches', 'value': 3})
        },
        {
            'name': 'Speed Demon',
            'description': 'Solve a challenge in under 30 seconds',
            'icon': 'bi-lightning-charge-fill',
            'points': 20,
            'criteria': json.dumps({'type': 'fastest_time', 'value': 30})
        },
        {
            'name': 'Veteran',
            'description': 'Complete 50 matches',
            'icon': 'bi-shield-fill',
            'points': 15,
            'criteria': json.dumps({'type': 'total_matches', 'value': 50})
        },
        {
            'name': 'Master Coder',
            'description': 'Solve 10 different challenges',
            'icon': 'bi-code-slash',
            'points': 50,
            'criteria': json.dumps({'type': 'unique_challenges', 'value': 10})
        },
        {
            'name': 'Challenge Accepted',
            'description': 'Complete at least one challenge of each difficulty',
            'icon': 'bi-trophy',
            'points': 40,
            'criteria': json.dumps({'type': 'all_difficulties', 'value': True})
        },
        {
            'name': 'Social Butterfly',
            'description': 'Add 10 friends',
            'icon': 'bi-people-fill',
            'points': 15,
            'criteria': json.dumps({'type': 'friends', 'value': 10})
        },
        {
            'name': 'Comeback King',
            'description': 'Win after losing 3 matches in a row',
            'icon': 'bi-arrow-up-circle-fill',
            'points': 25,
            'criteria': json.dumps({'type': 'comeback', 'value': 3})
        },
        {
            'name': 'No Mercy',
            'description': 'Win 10 matches in a row',
            'icon': 'bi-lightning-fill',
            'points': 35,
            'criteria': json.dumps({'type': 'win_streak', 'value': 10})
        }
    ]
    
    for achievement_data in achievements_data:
        # Check if achievement already exists
        existing = Achievement.query.filter_by(name=achievement_data['name']).first()
        if not existing:
            achievement = Achievement(**achievement_data)
            db.session.add(achievement)
    
    db.session.commit()
    print(f"Seeded {len(achievements_data)} achievements")

def seed_learning_modules():
    """Seed learning modules and lessons"""
    print("\nSeeding learning modules...")
    
    # Clear existing learning data
    Lesson.query.delete()
    Module.query.delete()
    db.session.commit()
    
    # Module 1: Python Basics
    module1 = Module(
        title="Python Basics",
        description="Start your Python journey! Learn variables, data types, and basic operations.",
        icon="bi-rocket-takeoff",
        difficulty="Beginner",
        order=1,
        estimated_hours=3
    )
    db.session.add(module1)
    db.session.flush()
    
    # Lesson 1.1: Hello World & Print
    lesson1_1 = Lesson(
        module_id=module1.id,
        title="Hello World & Print Function",
        order=1,
        estimated_minutes=15,
        reading_content="""
<h3>Welcome to Python!</h3>
<p>The <code>print()</code> function is your first tool for displaying output in Python. It's one of the most used functions!</p>

<h4>Basic Syntax:</h4>
<pre><code>print("Hello, World!")</code></pre>

<p>You can print multiple items by separating them with commas:</p>
<pre><code>print("Hello", "World", "!")
# Output: Hello World !</code></pre>

<p>The <code>print()</code> function automatically adds spaces between items and a newline at the end.</p>

<h4>Printing Numbers:</h4>
<pre><code>print(42)
print(3.14)
print(100 + 50)  # Output: 150</code></pre>

<h4>Special Characters:</h4>
<ul>
    <li><code>\\n</code> - New line</li>
    <li><code>\\t</code> - Tab</li>
    <li><code>\\"</code> - Quote character</li>
</ul>

<pre><code>print("Line 1\\nLine 2\\nLine 3")</code></pre>
        """,
        starter_code='# Write code to print "Hello, Python!"\n',
        solution_code='print("Hello, Python!")',
    )
    
    lesson1_1.set_learning_objectives([
        "Understand how to use the print() function",
        "Display text and numbers in Python",
        "Use special characters in strings"
    ])
    lesson1_1.set_key_concepts(["print()", "Strings", "Output"])
    lesson1_1.set_test_cases([
        {
            "name": "Test 1: Print exact message",
            "input": "",
            "expected_output": "Hello, Python!"
        }
    ])
    lesson1_1.set_hints([
        "Use the print() function",
        'Put your text in quotes: print("text")',
        'The exact message is: Hello, Python!'
    ])
    lesson1_1.set_visual_content({
        "animation": {
            "type": "code_flow",
            "steps": [
                {"step": 1, "description": "Python reads the print() function call"},
                {"step": 2, "description": "Evaluates the string inside quotes"},
                {"step": 3, "description": "Outputs the text to the console"}
            ]
        }
    })
    db.session.add(lesson1_1)
    
    # Lesson 1.2: Variables and Data Types
    lesson1_2 = Lesson(
        module_id=module1.id,
        title="Variables and Data Types",
        order=2,
        estimated_minutes=20,
        reading_content="""
<h3>What are Variables?</h3>
<p>Variables are containers for storing data values. Think of them as labeled boxes where you can keep information.</p>

<h4>Creating Variables:</h4>
<pre><code>name = "Alice"
age = 25
height = 5.7
is_student = True</code></pre>

<h4>Python Data Types:</h4>
<ul>
    <li><strong>str</strong> (String): Text data - <code>"Hello"</code></li>
    <li><strong>int</strong> (Integer): Whole numbers - <code>42</code></li>
    <li><strong>float</strong> (Float): Decimal numbers - <code>3.14</code></li>
    <li><strong>bool</strong> (Boolean): True or False - <code>True</code></li>
</ul>

<h4>Variable Naming Rules:</h4>
<ul>
    <li>Must start with a letter or underscore</li>
    <li>Can contain letters, numbers, and underscores</li>
    <li>Case-sensitive (age and Age are different)</li>
    <li>Cannot use Python keywords (if, for, while, etc.)</li>
</ul>

<h4>Using Variables:</h4>
<pre><code>name = "Bob"
age = 30
print(name, "is", age, "years old")
# Output: Bob is 30 years old</code></pre>

<h4>Type Checking:</h4>
<pre><code>x = 5
print(type(x))  # Output: &lt;class 'int'&gt;</code></pre>
        """,
        starter_code='# Create a variable called "message" with the text "Python is awesome"\n# Then print the variable\n',
        solution_code='message = "Python is awesome"\nprint(message)',
    )
    
    lesson1_2.set_learning_objectives([
        "Create and use variables in Python",
        "Understand different data types (str, int, float, bool)",
        "Follow variable naming conventions"
    ])
    lesson1_2.set_key_concepts(["Variables", "Data Types", "Assignment", "type()"])
    lesson1_2.set_test_cases([
        {
            "name": "Test 1: Create and print variable",
            "input": "",
            "expected_output": "Python is awesome"
        }
    ])
    lesson1_2.set_hints([
        "Create a variable using: variable_name = value",
        'Use quotes for text: message = "text here"',
        'Print the variable: print(message)'
    ])
    db.session.add(lesson1_2)
    
    # Lesson 1.3: Basic Math Operations
    lesson1_3 = Lesson(
        module_id=module1.id,
        title="Basic Math Operations",
        order=3,
        estimated_minutes=20,
        reading_content="""
<h3>Python as a Calculator</h3>
<p>Python can perform all basic mathematical operations and more!</p>

<h4>Arithmetic Operators:</h4>
<pre><code># Addition
print(10 + 5)   # 15

# Subtraction
print(10 - 5)   # 5

# Multiplication
print(10 * 5)   # 50

# Division (always returns float)
print(10 / 3)   # 3.333...

# Floor Division (returns integer)
print(10 // 3)  # 3

# Modulus (remainder)
print(10 % 3)   # 1

# Exponentiation (power)
print(2 ** 3)   # 8</code></pre>

<h4>Order of Operations (PEMDAS):</h4>
<p>Python follows standard mathematical order:</p>
<ol>
    <li>Parentheses</li>
    <li>Exponents</li>
    <li>Multiplication/Division</li>
    <li>Addition/Subtraction</li>
</ol>

<pre><code>result = (5 + 3) * 2
print(result)  # 16 (not 11)

result = 5 + 3 * 2
print(result)  # 11 (not 16)</code></pre>
        """,
        starter_code='# Calculate and print: (15 + 25) * 2\n',
        solution_code='result = (15 + 25) * 2\nprint(result)',
    )
    
    lesson1_3.set_learning_objectives([
        "Perform basic arithmetic operations",
        "Understand operator precedence",
        "Use shorthand assignment operators"
    ])
    lesson1_3.set_key_concepts(["Arithmetic Operators", "+, -, *, /, //, %, **", "PEMDAS"])
    lesson1_3.set_test_cases([
        {
            "name": "Test 1: Calculate (15 + 25) * 2",
            "input": "",
            "expected_output": "80"
        }
    ])
    lesson1_3.set_hints([
        "Use parentheses for the addition first",
        "Multiply the result by 2",
        "Print the final result"
    ])
    db.session.add(lesson1_3)
    
    # Module 2: Control Flow
    module2 = Module(
        title="Control Flow",
        description="Learn to make decisions in code with if statements and loops!",
        icon="bi-signpost-split",
        difficulty="Beginner",
        order=2,
        estimated_hours=4
    )
    db.session.add(module2)
    db.session.flush()
    
    # Lesson 2.1: If Statements
    lesson2_1 = Lesson(
        module_id=module2.id,
        title="If Statements and Conditions",
        order=1,
        estimated_minutes=25,
        reading_content="""
<h3>Making Decisions in Code</h3>
<p>If statements allow your program to make decisions based on conditions.</p>

<h4>Basic If Statement:</h4>
<pre><code>age = 18
if age >= 18:
    print("You are an adult")</code></pre>

<h4>If-Else:</h4>
<pre><code>age = 15
if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")</code></pre>

<p><strong>Important:</strong> Indentation matters in Python! Code inside if blocks must be indented.</p>
        """,
        starter_code='# Write code that checks if a number is positive\n# If number > 0, print "Positive"\n# Otherwise print "Not positive"\nnumber = 5\n',
        solution_code='number = 5\nif number > 0:\n    print("Positive")\nelse:\n    print("Not positive")',
    )
    
    lesson2_1.set_learning_objectives([
        "Write if, elif, and else statements",
        "Use comparison operators",
        "Understand Python indentation"
    ])
    lesson2_1.set_key_concepts(["if/elif/else", "Comparison Operators", "Indentation"])
    lesson2_1.set_test_cases([
        {
            "name": "Test 1: Positive number",
            "input": "",
            "expected_output": "Positive"
        }
    ])
    lesson2_1.set_hints([
        "Use if number > 0:",
        "Remember to indent the print statement",
        "Use else: for the other case"
    ])
    db.session.add(lesson2_1)
    
    # Lesson 2.2: For Loops
    lesson2_2 = Lesson(
        module_id=module2.id,
        title="For Loops - Repeat Actions",
        order=2,
        estimated_minutes=25,
        reading_content="""
<h3>Repeating Code with For Loops</h3>
<p>For loops let you repeat code a specific number of times.</p>

<h4>Basic For Loop with range():</h4>
<pre><code># Print numbers 0 to 4
for i in range(5):
    print(i)
# Output: 0, 1, 2, 3, 4</code></pre>

<h4>Range with Start and End:</h4>
<pre><code># Print numbers 1 to 5
for i in range(1, 6):
    print(i)
# Output: 1, 2, 3, 4, 5</code></pre>
        """,
        starter_code='# Use a for loop to print numbers 1 to 10\n',
        solution_code='for i in range(1, 11):\n    print(i)',
    )
    
    lesson2_2.set_learning_objectives([
        "Write for loops using range()",
        "Iterate over sequences"
    ])
    lesson2_2.set_key_concepts(["for loop", "range()", "Iteration"])
    lesson2_2.set_test_cases([
        {
            "name": "Test 1: Print 1 to 10",
            "input": "",
            "expected_output": "1\n2\n3\n4\n5\n6\n7\n8\n9\n10"
        }
    ])
    lesson2_2.set_hints([
        "Use for i in range():",
        "range(1, 11) gives numbers 1 to 10",
        "Don't forget to print(i) inside the loop"
    ])
    db.session.add(lesson2_2)
    
    # Module 3: Data Structures
    module3 = Module(
        title="Data Structures",
        description="Master lists, dictionaries, tuples, and sets to organize your data efficiently.",
        icon="bi-diagram-3",
        difficulty="Intermediate",
        order=3,
        estimated_hours=5
    )
    db.session.add(module3)
    db.session.flush()
    
    # Lesson 3.1: Lists
    lesson3_1 = Lesson(
        module_id=module3.id,
        title="Lists - Ordered Collections",
        order=1,
        estimated_minutes=30,
        reading_content="""
<h3>Working with Lists</h3>
<p>Lists are ordered, mutable collections that can hold items of different types.</p>

<h4>Creating Lists:</h4>
<pre><code>numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "cherry"]</code></pre>

<h4>Modifying Lists:</h4>
<pre><code>fruits = ["apple", "banana"]
fruits.append("cherry")  # Add to end</code></pre>
        """,
        starter_code='# Create a list with numbers 1, 2, 3\n# Add the number 4 to the list\n# Print the entire list\n',
        solution_code='my_list = [1, 2, 3]\nmy_list.append(4)\nprint(my_list)',
    )
    
    lesson3_1.set_learning_objectives([
        "Create and access list elements",
        "Use list methods (append, insert, remove, etc.)"
    ])
    lesson3_1.set_key_concepts(["Lists", "Indexing", "append()"])
    lesson3_1.set_test_cases([
        {
            "name": "Test 1: List with 4 elements",
            "input": "",
            "expected_output": "[1, 2, 3, 4]"
        }
    ])
    lesson3_1.set_hints([
        "Create a list using square brackets: [1, 2, 3]",
        "Use my_list.append(4) to add an item",
        "Print the list: print(my_list)"
    ])
    db.session.add(lesson3_1)
    
    # Module 4: Functions
    module4 = Module(
        title="Functions",
        description="Write reusable code with functions, parameters, and return values.",
        icon="bi-box-seam",
        difficulty="Intermediate",
        order=4,
        estimated_hours=4
    )
    db.session.add(module4)
    db.session.flush()
    
    # Lesson 4.1: Defining Functions
    lesson4_1 = Lesson(
        module_id=module4.id,
        title="Creating Your First Function",
        order=1,
        estimated_minutes=25,
        reading_content="""
<h3>What are Functions?</h3>
<p>Functions are reusable blocks of code that perform specific tasks.</p>

<h4>Defining a Function:</h4>
<pre><code>def greet():
    print("Hello, World!")

greet()  # Call the function</code></pre>

<h4>Return Values:</h4>
<pre><code>def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: 8</code></pre>
        """,
        starter_code='# Define a function called "multiply" that takes two parameters\n# The function should return the product of the two numbers\n# Call it with 6 and 7 and print the result\n',
        solution_code='def multiply(a, b):\n    return a * b\n\nresult = multiply(6, 7)\nprint(result)',
    )
    
    lesson4_1.set_learning_objectives([
        "Define functions using def keyword",
        "Return values from functions"
    ])
    lesson4_1.set_key_concepts(["def", "Parameters", "return"])
    lesson4_1.set_test_cases([
        {
            "name": "Test 1: Multiply 6 and 7",
            "input": "",
            "expected_output": "42"
        }
    ])
    lesson4_1.set_hints([
        "Use def multiply(a, b): to define the function",
        "Return the product: return a * b",
        "Call it: result = multiply(6, 7) then print(result)"
    ])
    db.session.add(lesson4_1)
    
    # Commit all changes
    db.session.commit()
    print(f"✅ Created {Module.query.count()} modules")
    print(f"✅ Created {Lesson.query.count()} lessons")
    print("\nModules created:")
    for module in Module.query.order_by(Module.order).all():
        print(f"  - {module.title} ({len(module.lessons)} lessons)")

def seed_all():
    """Seed all data"""
    seed_challenges()
    seed_achievements()
    seed_learning_modules()
    print("\n🎉 Database seeding completed!")

if __name__ == '__main__':
    from app import app
    with app.app_context():
        seed_all()
