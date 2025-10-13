"""Learning module models for Python education"""
from datetime import datetime
import json
from . import db


class Module(db.Model):
    """Learning modules (e.g., Python Basics, Data Structures, Algorithms)"""
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='bi-book')
    difficulty = db.Column(db.String(20), nullable=False)  # Beginner, Intermediate, Advanced
    order = db.Column(db.Integer, default=0)
    estimated_hours = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    lessons = db.relationship('Lesson', backref='module', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Module {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'icon': self.icon,
            'difficulty': self.difficulty,
            'order': self.order,
            'estimated_hours': self.estimated_hours,
            'lesson_count': len(self.lessons)
        }


class Lesson(db.Model):
    """Individual lessons within modules"""
    __tablename__ = 'lessons'
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    order = db.Column(db.Integer, default=0)
    
    # Content for different learning styles
    reading_content = db.Column(db.Text)  # Markdown/HTML for reading learners
    visual_content = db.Column(db.Text)  # JSON with diagrams, flowcharts, animations
    video_url = db.Column(db.String(500))  # Optional video link
    
    # Hands-on coding exercises
    starter_code = db.Column(db.Text)
    solution_code = db.Column(db.Text)
    test_cases = db.Column(db.Text)  # JSON string with test cases
    hints = db.Column(db.Text)  # JSON array of progressive hints
    
    # Lesson metadata
    estimated_minutes = db.Column(db.Integer, default=15)
    learning_objectives = db.Column(db.Text)  # JSON array
    key_concepts = db.Column(db.Text)  # JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    progress_records = db.relationship('LessonProgress', backref='lesson', lazy=True)
    
    def __repr__(self):
        return f'<Lesson {self.title}>'
    
    def get_test_cases(self):
        """Parse JSON test cases"""
        return json.loads(self.test_cases) if self.test_cases else []
    
    def set_test_cases(self, test_cases_list):
        """Store test cases as JSON"""
        self.test_cases = json.dumps(test_cases_list)
    
    def get_hints(self):
        """Parse JSON hints"""
        return json.loads(self.hints) if self.hints else []
    
    def set_hints(self, hints_list):
        """Store hints as JSON"""
        self.hints = json.dumps(hints_list)
    
    def get_learning_objectives(self):
        """Parse JSON learning objectives"""
        return json.loads(self.learning_objectives) if self.learning_objectives else []
    
    def set_learning_objectives(self, objectives_list):
        """Store learning objectives as JSON"""
        self.learning_objectives = json.dumps(objectives_list)
    
    def get_key_concepts(self):
        """Parse JSON key concepts"""
        return json.loads(self.key_concepts) if self.key_concepts else []
    
    def set_key_concepts(self, concepts_list):
        """Store key concepts as JSON"""
        self.key_concepts = json.dumps(concepts_list)
    
    def get_visual_content(self):
        """Parse JSON visual content"""
        return json.loads(self.visual_content) if self.visual_content else {}
    
    def set_visual_content(self, visual_data):
        """Store visual content as JSON"""
        self.visual_content = json.dumps(visual_data)
    
    def to_dict(self):
        return {
            'id': self.id,
            'module_id': self.module_id,
            'title': self.title,
            'order': self.order,
            'estimated_minutes': self.estimated_minutes,
            'learning_objectives': self.get_learning_objectives(),
            'key_concepts': self.get_key_concepts()
        }


class LessonProgress(db.Model):
    """Track user progress through lessons"""
    __tablename__ = 'lesson_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lessons.id'), nullable=False)
    
    # Progress tracking
    status = db.Column(db.String(20), default='not_started')  # not_started, in_progress, completed
    completion_percentage = db.Column(db.Integer, default=0)
    
    # Interaction tracking
    hints_used = db.Column(db.Integer, default=0)
    attempts = db.Column(db.Integer, default=0)
    time_spent_minutes = db.Column(db.Integer, default=0)
    
    # Code submissions
    last_code_submission = db.Column(db.Text)
    passed_test_cases = db.Column(db.Integer, default=0)
    total_test_cases = db.Column(db.Integer, default=0)
    
    # Timestamps
    started_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint
    __table_args__ = (db.UniqueConstraint('user_id', 'lesson_id', name='unique_user_lesson'),)
    
    def __repr__(self):
        return f'<LessonProgress user={self.user_id} lesson={self.lesson_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'lesson_id': self.lesson_id,
            'status': self.status,
            'completion_percentage': self.completion_percentage,
            'hints_used': self.hints_used,
            'attempts': self.attempts,
            'time_spent_minutes': self.time_spent_minutes,
            'passed_test_cases': self.passed_test_cases,
            'total_test_cases': self.total_test_cases,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }


class Quiz(db.Model):
    """Quizzes for testing understanding"""
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    questions = db.Column(db.Text)  # JSON array of questions
    passing_score = db.Column(db.Integer, default=70)
    time_limit_minutes = db.Column(db.Integer, default=30)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_questions(self):
        """Parse JSON questions"""
        return json.loads(self.questions) if self.questions else []
    
    def set_questions(self, questions_list):
        """Store questions as JSON"""
        self.questions = json.dumps(questions_list)
    
    def __repr__(self):
        return f'<Quiz {self.title}>'


class QuizAttempt(db.Model):
    """Track quiz attempts"""
    __tablename__ = 'quiz_attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    score = db.Column(db.Integer)
    answers = db.Column(db.Text)  # JSON of user answers
    passed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_answers(self):
        """Parse JSON answers"""
        return json.loads(self.answers) if self.answers else {}
    
    def set_answers(self, answers_dict):
        """Store answers as JSON"""
        self.answers = json.dumps(answers_dict)
    
    def __repr__(self):
        return f'<QuizAttempt user={self.user_id} quiz={self.quiz_id}>'
