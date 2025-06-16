"""
API routes for AetherCode application
"""
from flask import Blueprint, request, jsonify
from datetime import datetime

# Import services
from app.services.code_executor import run_code
from app.services.code_analyzer import analyze_code
from app.services.code_reviewer import generate_review
from app.services.chat_service import process_chat_message
from app.services.file_handler import process_uploaded_files
from app.services.ai_service import generate_documentation, generate_tests

api_bp = Blueprint('api', __name__)

@api_bp.route('/execute', methods=['POST'])
def execute_code():
    """Execute code in the specified language and return the output"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        result = run_code(code, language)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/chat', methods=['POST'])
def chat():
    """Process chat messages and return AI responses"""
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = process_chat_message(message)
        return jsonify(response)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/review', methods=['POST'])
def review_code():
    """Analyze and review code"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        # Perform code analysis
        analysis_results = analyze_code(code, language)
        
        # Generate review based on analysis
        review = generate_review(code, language, analysis_results)
        
        return jsonify({'review': review})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/documentation', methods=['POST'])
def create_documentation():
    """Generate technical documentation for a project"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    format_type = data.get('format', 'markdown')
    sections = data.get('sections', ['api', 'architecture', 'requirements'])
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        # Use the AI service to generate documentation
        documentation = generate_documentation(code, language)
        
        # Add timestamp
        documentation['generated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        documentation['format'] = format_type
        documentation['sections'] = sections
        
        return jsonify({'documentation': documentation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tests', methods=['POST'])
def create_tests():
    """Generate test cases for code"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    framework = data.get('framework', 'pytest')
    test_types = data.get('test_types', ['unit'])
    scenarios = data.get('scenarios', '')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        # Use the AI service to generate tests
        tests = generate_tests(code, language, framework)
        
        # Add timestamp and additional info
        tests['generated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        tests['test_types'] = test_types
        tests['scenarios'] = scenarios
        
        return jsonify({'tests': tests})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/upload', methods=['POST'])
def upload_files():
    """Handle file uploads for analysis"""
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    try:
        result = process_uploaded_files(files)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
