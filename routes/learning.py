"""Learning module routes"""
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import json
from models import db
from models.user import User
from models.learning import Module, Lesson, LessonProgress, Quiz, QuizAttempt
from utils.code_testing import test_code


learning_bp = Blueprint('learning', __name__, url_prefix='/learn')


def login_required(f):
    """Decorator to require login"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@learning_bp.route('/')
@login_required
def index():
    """Display all learning modules"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    # Get all modules ordered by order field
    modules = Module.query.order_by(Module.order).all()
    
    # Calculate progress for each module
    module_progress = {}
    for module in modules:
        total_lessons = len(module.lessons)
        if total_lessons > 0:
            completed_lessons = LessonProgress.query.filter_by(
                user_id=user_id,
                status='completed'
            ).join(Lesson).filter(Lesson.module_id == module.id).count()
            
            progress_percentage = int((completed_lessons / total_lessons) * 100)
            module_progress[module.id] = {
                'total': total_lessons,
                'completed': completed_lessons,
                'percentage': progress_percentage
            }
        else:
            module_progress[module.id] = {
                'total': 0,
                'completed': 0,
                'percentage': 0
            }
    
    return render_template('learn.html', 
                         user=user,
                         modules=modules,
                         module_progress=module_progress)


@learning_bp.route('/module/<int:module_id>')
@login_required
def module_detail(module_id):
    """Display lessons in a module"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    module = Module.query.get_or_404(module_id)
    
    # Get all lessons ordered by order field
    lessons = Lesson.query.filter_by(module_id=module_id).order_by(Lesson.order).all()
    
    # Get progress for each lesson
    lesson_progress = {}
    for lesson in lessons:
        progress = LessonProgress.query.filter_by(
            user_id=user_id,
            lesson_id=lesson.id
        ).first()
        
        if progress:
            lesson_progress[lesson.id] = progress.to_dict()
        else:
            lesson_progress[lesson.id] = {
                'status': 'not_started',
                'completion_percentage': 0
            }
    
    return render_template('module.html',
                         user=user,
                         module=module,
                         lessons=lessons,
                         lesson_progress=lesson_progress)


@learning_bp.route('/lesson/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    """Display a lesson with interactive content"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    lesson = Lesson.query.get_or_404(lesson_id)
    module = lesson.module
    
    # Get or create progress record
    progress = LessonProgress.query.filter_by(
        user_id=user_id,
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            status='in_progress',
            started_at=datetime.utcnow()
        )
        db.session.add(progress)
        db.session.commit()
    else:
        # Update last accessed
        progress.last_accessed = datetime.utcnow()
        if progress.status == 'not_started':
            progress.status = 'in_progress'
            progress.started_at = datetime.utcnow()
        db.session.commit()
    
    # Get next and previous lessons for navigation
    all_lessons = Lesson.query.filter_by(module_id=module.id).order_by(Lesson.order).all()
    lesson_index = next((i for i, l in enumerate(all_lessons) if l.id == lesson_id), None)
    
    prev_lesson = all_lessons[lesson_index - 1] if lesson_index and lesson_index > 0 else None
    next_lesson = all_lessons[lesson_index + 1] if lesson_index is not None and lesson_index < len(all_lessons) - 1 else None
    
    return render_template('lesson.html',
                         user=user,
                         lesson=lesson,
                         module=module,
                         progress=progress,
                         prev_lesson=prev_lesson,
                         next_lesson=next_lesson)


@learning_bp.route('/lesson/<int:lesson_id>/submit', methods=['POST'])
@login_required
def submit_code(lesson_id):
    """Submit code for testing"""
    user_id = session.get('user_id')
    lesson = Lesson.query.get_or_404(lesson_id)
    
    data = request.get_json()
    user_code = data.get('code', '')
    
    # Get progress record
    progress = LessonProgress.query.filter_by(
        user_id=user_id,
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        return jsonify({'error': 'Progress record not found'}), 400
    
    # Update attempts
    progress.attempts += 1
    progress.last_code_submission = user_code
    
    # Get test cases
    test_cases = lesson.get_test_cases()
    
    if not test_cases:
        return jsonify({'error': 'No test cases available'}), 400
    
    # Run tests
    results = []
    passed_count = 0
    
    for i, test_case in enumerate(test_cases):
        test_input = test_case.get('input', '')
        expected_output = test_case.get('expected_output', '')
        test_name = test_case.get('name', f'Test {i+1}')
        
        result = test_code(user_code, test_input, expected_output)
        results.append({
            'name': test_name,
            'passed': result['passed'],
            'output': result['output'],
            'error': result.get('error', ''),
            'expected': expected_output
        })
        
        if result['passed']:
            passed_count += 1
    
    # Update progress
    progress.passed_test_cases = passed_count
    progress.total_test_cases = len(test_cases)
    progress.completion_percentage = int((passed_count / len(test_cases)) * 100)
    
    # Mark as completed if all tests pass
    if passed_count == len(test_cases):
        progress.status = 'completed'
        progress.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'results': results,
        'passed': passed_count,
        'total': len(test_cases),
        'completion_percentage': progress.completion_percentage,
        'all_passed': passed_count == len(test_cases)
    })


@learning_bp.route('/lesson/<int:lesson_id>/hint', methods=['POST'])
@login_required
def get_hint(lesson_id):
    """Get a progressive hint"""
    user_id = session.get('user_id')
    lesson = Lesson.query.get_or_404(lesson_id)
    
    # Get progress record
    progress = LessonProgress.query.filter_by(
        user_id=user_id,
        lesson_id=lesson_id
    ).first()
    
    if not progress:
        return jsonify({'error': 'Progress record not found'}), 400
    
    hints = lesson.get_hints()
    
    if not hints or progress.hints_used >= len(hints):
        return jsonify({'error': 'No more hints available'}), 400
    
    # Return the next hint
    hint = hints[progress.hints_used]
    progress.hints_used += 1
    db.session.commit()
    
    return jsonify({
        'success': True,
        'hint': hint,
        'hints_used': progress.hints_used,
        'total_hints': len(hints)
    })


@learning_bp.route('/lesson/<int:lesson_id>/reset', methods=['POST'])
@login_required
def reset_lesson(lesson_id):
    """Reset lesson progress"""
    user_id = session.get('user_id')
    
    progress = LessonProgress.query.filter_by(
        user_id=user_id,
        lesson_id=lesson_id
    ).first()
    
    if progress:
        progress.status = 'in_progress'
        progress.completion_percentage = 0
        progress.hints_used = 0
        progress.attempts = 0
        progress.passed_test_cases = 0
        progress.last_code_submission = None
        progress.completed_at = None
        db.session.commit()
    
    return jsonify({'success': True})


@learning_bp.route('/lesson/<int:lesson_id>/solution', methods=['GET'])
@login_required
def get_solution(lesson_id):
    """Get the solution code (only after several attempts)"""
    user_id = session.get('user_id')
    lesson = Lesson.query.get_or_404(lesson_id)
    
    progress = LessonProgress.query.filter_by(
        user_id=user_id,
        lesson_id=lesson_id
    ).first()
    
    # Require at least 3 attempts before showing solution
    if not progress or progress.attempts < 3:
        return jsonify({
            'error': 'You need to make at least 3 attempts before viewing the solution',
            'attempts': progress.attempts if progress else 0
        }), 403
    
    return jsonify({
        'success': True,
        'solution': lesson.solution_code
    })


@learning_bp.route('/progress')
@login_required
def user_progress():
    """View overall learning progress"""
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    # Get all modules with progress
    modules = Module.query.order_by(Module.order).all()
    
    progress_summary = []
    total_lessons = 0
    completed_lessons = 0
    
    for module in modules:
        module_lessons = len(module.lessons)
        total_lessons += module_lessons
        
        if module_lessons > 0:
            module_completed = LessonProgress.query.filter_by(
                user_id=user_id,
                status='completed'
            ).join(Lesson).filter(Lesson.module_id == module.id).count()
            
            completed_lessons += module_completed
            
            progress_summary.append({
                'module': module,
                'total_lessons': module_lessons,
                'completed_lessons': module_completed,
                'percentage': int((module_completed / module_lessons) * 100)
            })
    
    overall_percentage = int((completed_lessons / total_lessons) * 100) if total_lessons > 0 else 0
    
    # Get recent activity
    recent_lessons = LessonProgress.query.filter_by(user_id=user_id)\
        .order_by(LessonProgress.last_accessed.desc())\
        .limit(5).all()
    
    return render_template('learn_progress.html',
                         user=user,
                         progress_summary=progress_summary,
                         total_lessons=total_lessons,
                         completed_lessons=completed_lessons,
                         overall_percentage=overall_percentage,
                         recent_lessons=recent_lessons)


@learning_bp.route('/api/modules')
def api_modules():
    """API endpoint for modules list"""
    modules = Module.query.order_by(Module.order).all()
    return jsonify([m.to_dict() for m in modules])


@learning_bp.route('/api/module/<int:module_id>/lessons')
def api_module_lessons(module_id):
    """API endpoint for lessons in a module"""
    lessons = Lesson.query.filter_by(module_id=module_id).order_by(Lesson.order).all()
    return jsonify([l.to_dict() for l in lessons])
