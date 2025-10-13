"""
Database seeding script for CodeClash
Seeds challenges, achievements, and learning modules into the database
Loads data from JSON files in the data/ directory
"""
from models import db, Challenge, Achievement
from models.learning import Module, Lesson
import json
import os
import glob

def load_json_files(pattern):
    """Load JSON files matching the pattern"""
    files = sorted(glob.glob(pattern))
    data = []
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            data.append(json.load(f))
    return data

def calculate_reading_time(reading_content, starter_code='', solution_code=''):
    """
    Calculate estimated reading time in minutes based on content length.
    
    Average reading speed: 200-250 words per minute
    Code reading is slower: ~100-150 words per minute
    We'll use conservative estimates and add base time for hands-on practice.
    
    Args:
        reading_content: HTML content with explanations
        starter_code: Starting code to understand
        solution_code: Solution code to review
    
    Returns:
        int: Estimated time in minutes (minimum 5, maximum 60)
    """
    import re
    
    # Remove HTML tags to get actual text content
    text_content = re.sub(r'<[^>]+>', '', reading_content)
    
    # Count words in text content
    text_words = len(text_content.split())
    
    # Count lines of code (non-empty, non-comment)
    code_lines = 0
    for code in [starter_code, solution_code]:
        if code:
            lines = [line.strip() for line in code.split('\n') 
                    if line.strip() and not line.strip().startswith('#')]
            code_lines += len(lines)
    
    # Calculate reading time
    # Text: 200 words per minute
    # Code: 50 words per line, 150 words per minute = ~3 lines per minute
    text_time = text_words / 200
    code_time = code_lines / 3
    
    # Add base time for practice (5 minutes minimum)
    total_time = text_time + code_time + 5
    
    # Round to nearest 5 minutes and enforce bounds
    estimated_minutes = max(5, min(60, round(total_time / 5) * 5))
    
    return estimated_minutes

def seed_challenges():
    """Seed initial challenges from JSON files"""
    print("Loading challenges from JSON files...")
    challenges_data = load_json_files('data/challenges/*.json')
    
    for challenge_data in challenges_data:
        # Check if challenge already exists
        existing = Challenge.query.filter_by(title=challenge_data['title']).first()
        if not existing:
            # Convert test_cases list to JSON string for database
            challenge_data['test_cases'] = json.dumps(challenge_data['test_cases'])
            challenge = Challenge(**challenge_data)
            db.session.add(challenge)
    
    db.session.commit()
    print(f"✅ Seeded {len(challenges_data)} challenges")

def seed_achievements():
    """Seed achievements from JSON files"""
    print("Loading achievements from JSON files...")
    achievements_data = load_json_files('data/achievements/*.json')
    
    for achievement_data in achievements_data:
        # Check if achievement already exists
        existing = Achievement.query.filter_by(name=achievement_data['name']).first()
        if not existing:
            # Convert criteria dict to JSON string for database
            achievement_data['criteria'] = json.dumps(achievement_data['criteria'])
            achievement = Achievement(**achievement_data)
            db.session.add(achievement)
    
    db.session.commit()
    print(f"✅ Seeded {len(achievements_data)} achievements")

def seed_learning_modules():
    """Seed learning modules and lessons from JSON files"""
    print("\n" + "="*50)
    print("Loading learning modules from JSON files...")
    print("="*50)
    
    # Clear existing learning data (delete child records first due to foreign keys)
    from models.learning import LessonProgress
    LessonProgress.query.delete()
    Lesson.query.delete()
    Module.query.delete()
    db.session.commit()
    
    # Load modules from JSON files
    modules_data = load_json_files('data/modules/*.json')
    module_map = {}  # Map to store module_id mapping (order -> actual id)
    module_objects = {}  # Store module objects to update estimated_hours later
    
    print(f"\nCreating {len(modules_data)} modules...")
    for module_data in modules_data:
        # Don't use estimated_hours from JSON - will calculate from lessons
        if 'estimated_hours' in module_data:
            del module_data['estimated_hours']
        
        module = Module(**module_data, estimated_hours=0)  # Temporary value
        db.session.add(module)
        db.session.flush()  # Get the ID
        module_map[module_data['order']] = module.id
        module_objects[module_data['order']] = module
        print(f"  ✓ {module.title} (ID: {module.id})")
    
    # Load lessons from all module folders
    lessons_created = 0
    lesson_folders = sorted(glob.glob('data/lessons/*'))
    module_lesson_times = {}  # Track total minutes per module
    
    print(f"\nCreating lessons from {len(lesson_folders)} folders...")
    for lesson_folder in lesson_folders:
        folder_name = os.path.basename(lesson_folder)
        # Extract module order from folder name (e.g., "01-python-basics" -> 1)
        module_order = int(folder_name.split('-')[0])
        
        # Get lessons in this folder
        lesson_files = load_json_files(f'{lesson_folder}/*.json')
        
        for lesson_data in lesson_files:
            # Map the module_id from order to actual database ID
            lesson_data['module_id'] = module_map[module_order]
            
            # Calculate estimated reading time based on content
            reading_content = lesson_data.get('reading_content', '')
            starter_code = lesson_data.get('starter_code', '')
            solution_code = lesson_data.get('solution_code', '')
            
            estimated_minutes = calculate_reading_time(
                reading_content, 
                starter_code, 
                solution_code
            )
            
            # Create the lesson
            lesson = Lesson(
                module_id=lesson_data['module_id'],
                title=lesson_data['title'],
                order=lesson_data['order'],
                estimated_minutes=estimated_minutes,
                reading_content=reading_content,
                starter_code=starter_code,
                solution_code=solution_code
            )
            
            # Set the JSON-based fields using the setter methods
            if 'learning_objectives' in lesson_data:
                lesson.set_learning_objectives(lesson_data['learning_objectives'])
            if 'key_concepts' in lesson_data:
                lesson.set_key_concepts(lesson_data['key_concepts'])
            if 'test_cases' in lesson_data:
                lesson.set_test_cases(lesson_data['test_cases'])
            if 'hints' in lesson_data:
                lesson.set_hints(lesson_data['hints'])
            if 'visual_content' in lesson_data:
                lesson.set_visual_content(lesson_data['visual_content'])
            
            db.session.add(lesson)
            lessons_created += 1
            
            # Track total time for this module
            if module_order not in module_lesson_times:
                module_lesson_times[module_order] = 0
            module_lesson_times[module_order] += estimated_minutes
            
            print(f"    ✓ {lesson.title} ({estimated_minutes} min)")
    
    # Update module estimated_hours based on cumulative lesson times
    print(f"\nCalculating module estimated hours...")
    for module_order, total_minutes in module_lesson_times.items():
        module = module_objects[module_order]
        estimated_hours = round(total_minutes / 60, 1)  # Convert to hours with 1 decimal
        module.estimated_hours = estimated_hours
        print(f"  ✓ {module.title}: {total_minutes} min = {estimated_hours} hours")
    
    # Commit all changes
    db.session.commit()
    
    print("\n" + "="*50)
    print(f"✅ Created {Module.query.count()} modules")
    print(f"✅ Created {Lesson.query.count()} lessons")
    print("="*50)
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