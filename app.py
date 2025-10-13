"""
CodeClash - Competitive Programming Platform
Main application entry point with refactored structure
"""
from config import create_app
from routes import register_blueprints

# Create Flask app using factory
app = create_app()

# Register all route blueprints
register_blueprints(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
