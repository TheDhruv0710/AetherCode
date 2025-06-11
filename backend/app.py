"""
AetherCode - Flask Backend for Code Analysis and AI Chat
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import logging
import tempfile
import shutil
from werkzeug.utils import secure_filename

# Import services
from services.code_analyzer import CodeAnalyzer
from services.ai_service import AIService
from services.code_executor import CodeExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize services
code_analyzer = CodeAnalyzer()
ai_service = AIService()
code_executor = CodeExecutor()

# API routes
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

# Chat endpoint is defined later in the file

@app.route('/api/execute', methods=['POST'])
def execute_code():
    """Execute code and return the output"""
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'javascript')
        
        if not code:
            return jsonify({
                'success': False,
                'error': 'No code provided'
            }), 400
        
        # Execute the code
        result = code_executor.execute(code, language)
        
        return jsonify({
            'success': result['success'],
            'output': result['output'],
            'error': result['error'],
            'execution_time': result['execution_time']
        })
        
    except Exception as e:
        app.logger.error(f"Error executing code: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Server error: {str(e)}"
        }), 500

@app.route('/api/analyze', methods=['POST'])
def analyze_code():
    """
    Analyze code submitted by the user
    Expects JSON with:
    - code: string (code content)
    - language: string (programming language)
    - filename: string (optional)
    """
    try:
        data = request.json
        
        if not data or 'code' not in data:
            return jsonify({"error": "No code provided"}), 400
            
        code = data.get('code', '')
        language = data.get('language', 'javascript')
        filename = data.get('filename', None)
        
        logger.info(f"Analyzing code in {language}")
        
        # Perform code analysis
        analysis_result = code_analyzer.analyze(code, language, filename)
        
        return jsonify(analysis_result), 200
        
    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Process a chat message from the user
    Expects JSON with:
    - message: string (user's message)
    - code: string (optional, current code in editor)
    - language: string (optional, programming language)
    - history: list (optional, previous messages)
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"success": False, "error": "No message provided"}), 400
            
        user_message = data.get('message', '')
        code = data.get('code', '')
        language = data.get('language', 'javascript')
        history = data.get('history', [])
        
        logger.info(f"Processing chat message: {user_message[:50]}...")
        
        # Get AI response
        ai_response = ai_service.get_response(
            user_message=user_message, 
            conversation_history=history, 
            code_context=code, 
            language=language
        )
        
        return jsonify({
            "success": True,
            "response": ai_response
        })
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Handle file uploads
    """
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
            
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
            
        if file:
            # Save the file temporarily
            temp_path = os.path.join('temp', file.filename)
            os.makedirs('temp', exist_ok=True)
            file.save(temp_path)
            
            # Read the file content
            with open(temp_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            # Determine language from file extension
            _, ext = os.path.splitext(file.filename)
            language = code_analyzer.detect_language(ext.lower()[1:])
            
            # Analyze the code
            analysis_result = code_analyzer.analyze(code, language, file.filename)
            
            # Clean up
            os.remove(temp_path)
            
            return jsonify({
                "filename": file.filename,
                "language": language,
                "analysis": analysis_result
            }), 200
            
    except Exception as e:
        logger.error(f"Error processing upload: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/project', methods=['POST'])
def upload_project():
    """
    Handle project uploads (multiple files)
    """
    try:
        if 'files[]' not in request.files:
            return jsonify({"error": "No files part"}), 400
            
        files = request.files.getlist('files[]')
        
        if not files or len(files) == 0:
            return jsonify({"error": "No files selected"}), 400
            
        project_analysis = []
        
        for file in files:
            if file.filename == '':
                continue
                
            # Save the file temporarily
            temp_path = os.path.join('temp', file.filename)
            os.makedirs('temp', exist_ok=True)
            file.save(temp_path)
            
            # Read the file content
            try:
                with open(temp_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                # Determine language from file extension
                _, ext = os.path.splitext(file.filename)
                language = code_analyzer.detect_language(ext.lower()[1:])
                
                # Analyze the code
                analysis_result = code_analyzer.analyze(code, language, file.filename)
                
                project_analysis.append({
                    "filename": file.filename,
                    "language": language,
                    "analysis": analysis_result
                })
                
            except Exception as e:
                logger.warning(f"Error processing file {file.filename}: {str(e)}")
                project_analysis.append({
                    "filename": file.filename,
                    "error": str(e)
                })
            
            # Clean up
            os.remove(temp_path)
        
        # Perform project-level analysis
        project_summary = code_analyzer.analyze_project(project_analysis)
        
        return jsonify({
            "files": project_analysis,
            "project_summary": project_summary
        }), 200
            
    except Exception as e:
        logger.error(f"Error processing project upload: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
