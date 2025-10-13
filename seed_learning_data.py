"""Seed learning module data with Python lessons"""
from app import app
from models import db
from models.learning import Module, Lesson
import json


def create_learning_data():
    """Create comprehensive Python learning modules and lessons"""
    
    with app.app_context():
        # Clear existing learning data
        print("Clearing existing learning data...")
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

<h4>Variables in Math:</h4>
<pre><code>x = 10
y = 3
sum_result = x + y
print(sum_result)  # 13</code></pre>

<h4>Shorthand Operators:</h4>
<pre><code>x = 10
x += 5  # Same as: x = x + 5
print(x)  # 15

x *= 2  # Same as: x = x * 2
print(x)  # 30</code></pre>
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

<h4>If-Elif-Else:</h4>
<pre><code>score = 85
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")</code></pre>

<h4>Comparison Operators:</h4>
<ul>
    <li><code>==</code> - Equal to</li>
    <li><code>!=</code> - Not equal to</li>
    <li><code>&gt;</code> - Greater than</li>
    <li><code>&lt;</code> - Less than</li>
    <li><code>&gt;=</code> - Greater than or equal</li>
    <li><code>&lt;=</code> - Less than or equal</li>
</ul>

<h4>Logical Operators:</h4>
<pre><code># AND - both conditions must be True
if age >= 18 and has_license:
    print("Can drive")

# OR - at least one condition must be True
if is_weekend or is_holiday:
    print("No work!")

# NOT - reverses the condition
if not is_raining:
    print("Go outside!")</code></pre>

<p><strong>Important:</strong> Indentation matters in Python! Code inside if blocks must be indented.</p>
            """,
            starter_code='# Write code that checks if a number is positive\n# If number > 0, print "Positive"\n# Otherwise print "Not positive"\nnumber = 5\n',
            solution_code='number = 5\nif number > 0:\n    print("Positive")\nelse:\n    print("Not positive")',
        )
        
        lesson2_1.set_learning_objectives([
            "Write if, elif, and else statements",
            "Use comparison operators",
            "Combine conditions with logical operators",
            "Understand Python indentation"
        ])
        
        lesson2_1.set_key_concepts(["if/elif/else", "Comparison Operators", "Logical Operators", "Indentation"])
        
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
<p>For loops let you repeat code a specific number of times or iterate over sequences.</p>

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

<h4>Range with Step:</h4>
<pre><code># Print even numbers 0 to 10
for i in range(0, 11, 2):
    print(i)
# Output: 0, 2, 4, 6, 8, 10</code></pre>

<h4>Looping Through Strings:</h4>
<pre><code>name = "Python"
for letter in name:
    print(letter)
# Output: P, y, t, h, o, n (each on new line)</code></pre>

<h4>Looping Through Lists:</h4>
<pre><code>fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)</code></pre>

<h4>Nested Loops:</h4>
<pre><code>for i in range(3):
    for j in range(2):
        print(f"i={i}, j={j}")</code></pre>

<h4>Loop Control:</h4>
<ul>
    <li><code>break</code> - Exit the loop early</li>
    <li><code>continue</code> - Skip to next iteration</li>
</ul>

<pre><code># Using break
for i in range(10):
    if i == 5:
        break
    print(i)  # Prints 0-4

# Using continue
for i in range(5):
    if i == 2:
        continue
    print(i)  # Prints 0, 1, 3, 4</code></pre>
            """,
            starter_code='# Use a for loop to print numbers 1 to 10\n',
            solution_code='for i in range(1, 11):\n    print(i)',
        )
        
        lesson2_2.set_learning_objectives([
            "Write for loops using range()",
            "Iterate over strings and lists",
            "Use break and continue statements",
            "Create nested loops"
        ])
        
        lesson2_2.set_key_concepts(["for loop", "range()", "Iteration", "break/continue"])
        
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
<pre><code># Empty list
my_list = []

# List with items
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", 3.14, True]</code></pre>

<h4>Accessing Elements:</h4>
<pre><code>fruits = ["apple", "banana", "cherry"]
print(fruits[0])   # apple (first item)
print(fruits[1])   # banana
print(fruits[-1])  # cherry (last item)
print(fruits[-2])  # banana (second from end)</code></pre>

<h4>List Slicing:</h4>
<pre><code>numbers = [0, 1, 2, 3, 4, 5]
print(numbers[1:4])   # [1, 2, 3]
print(numbers[:3])    # [0, 1, 2]
print(numbers[3:])    # [3, 4, 5]
print(numbers[::2])   # [0, 2, 4] (every 2nd item)</code></pre>

<h4>Modifying Lists:</h4>
<pre><code>fruits = ["apple", "banana"]

# Add items
fruits.append("cherry")        # Add to end
fruits.insert(1, "orange")     # Insert at index
fruits.extend(["mango", "grape"])  # Add multiple

# Remove items
fruits.remove("banana")        # Remove by value
popped = fruits.pop()          # Remove last item
del fruits[0]                  # Remove by index

# Change items
fruits[0] = "strawberry"</code></pre>

<h4>List Methods:</h4>
<ul>
    <li><code>len(list)</code> - Get length</li>
    <li><code>list.count(item)</code> - Count occurrences</li>
    <li><code>list.index(item)</code> - Find index</li>
    <li><code>list.sort()</code> - Sort in place</li>
    <li><code>list.reverse()</code> - Reverse in place</li>
    <li><code>list.clear()</code> - Remove all items</li>
</ul>

<h4>List Comprehension:</h4>
<pre><code># Create list of squares
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Filtered list
evens = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]</code></pre>
            """,
            starter_code='# Create a list with numbers 1, 2, 3\n# Add the number 4 to the list\n# Print the entire list\n',
            solution_code='my_list = [1, 2, 3]\nmy_list.append(4)\nprint(my_list)',
        )
        
        lesson3_1.set_learning_objectives([
            "Create and access list elements",
            "Use list methods (append, insert, remove, etc.)",
            "Slice lists to get sublists",
            "Write list comprehensions"
        ])
        
        lesson3_1.set_key_concepts(["Lists", "Indexing", "Slicing", "append()", "List Comprehension"])
        
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
<p>Functions are reusable blocks of code that perform specific tasks. They help organize code and avoid repetition.</p>

<h4>Defining a Function:</h4>
<pre><code>def greet():
    print("Hello, World!")

# Call the function
greet()  # Output: Hello, World!</code></pre>

<h4>Functions with Parameters:</h4>
<pre><code>def greet(name):
    print(f"Hello, {name}!")

greet("Alice")  # Output: Hello, Alice!
greet("Bob")    # Output: Hello, Bob!</code></pre>

<h4>Multiple Parameters:</h4>
<pre><code>def add(a, b):
    result = a + b
    print(result)

add(5, 3)  # Output: 8</code></pre>

<h4>Return Values:</h4>
<pre><code>def add(a, b):
    return a + b

result = add(5, 3)
print(result)  # Output: 8

# Use in expressions
total = add(10, 20) + add(5, 15)
print(total)  # Output: 50</code></pre>

<h4>Default Parameters:</h4>
<pre><code>def greet(name="Guest"):
    print(f"Hello, {name}!")

greet()         # Output: Hello, Guest!
greet("Alice")  # Output: Hello, Alice!</code></pre>

<h4>Function Documentation:</h4>
<pre><code>def calculate_area(width, height):
    """
    Calculate the area of a rectangle.
    
    Parameters:
        width (float): Width of rectangle
        height (float): Height of rectangle
    
    Returns:
        float: Area of rectangle
    """
    return width * height</code></pre>

<h4>Why Use Functions?</h4>
<ul>
    <li><strong>Reusability:</strong> Write once, use many times</li>
    <li><strong>Organization:</strong> Break complex problems into smaller pieces</li>
    <li><strong>Readability:</strong> Self-documenting code with descriptive names</li>
    <li><strong>Testing:</strong> Easier to test individual functions</li>
</ul>
            """,
            starter_code='# Define a function called "multiply" that takes two parameters\n# The function should return the product of the two numbers\n# Call it with 6 and 7 and print the result\n',
            solution_code='def multiply(a, b):\n    return a * b\n\nresult = multiply(6, 7)\nprint(result)',
        )
        
        lesson4_1.set_learning_objectives([
            "Define functions using def keyword",
            "Add parameters to functions",
            "Return values from functions",
            "Use default parameter values"
        ])
        
        lesson4_1.set_key_concepts(["def", "Parameters", "return", "Function Calls"])
        
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
        print(f"\n✅ Created {Module.query.count()} modules")
        print(f"✅ Created {Lesson.query.count()} lessons")
        print("\nModules created:")
        for module in Module.query.order_by(Module.order).all():
            print(f"  - {module.title} ({len(module.lessons)} lessons)")


if __name__ == '__main__':
    create_learning_data()
    print("\n🎉 Learning data seeded successfully!")
