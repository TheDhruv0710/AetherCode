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

@api_bp.route('/generate-documentation', methods=['POST'])
def generate_tech_spec():
    """Generate technical specification for a project based on description"""
    data = request.json
    description = data.get('description', '')
    output_format = data.get('outputFormat', 'markdown')
    sections = data.get('sections', [])
    
    if not description:
        return jsonify({'error': 'No project description provided'}), 400
    
    try:
        # In a real implementation, this would call an AI service
        # For now, we'll generate a mock response
        content = f"# Technical Specification\n\n## Project Overview\n\n{description}\n\n"
        
        if 'api-endpoints' in sections:
            content += "## API Endpoints\n\n- GET /api/items - Retrieve all items\n- GET /api/items/:id - Retrieve specific item\n- POST /api/items - Create new item\n- PUT /api/items/:id - Update existing item\n- DELETE /api/items/:id - Delete an item\n\n"
        
        if 'database-schema' in sections:
            content += "## Database Schema\n\n### Items Table\n- id: integer, primary key\n- name: string, not null\n- description: text\n- created_at: timestamp\n- updated_at: timestamp\n\n"
        
        if 'architecture' in sections:
            content += "## Architecture\n\nThe application follows a standard three-tier architecture:\n\n1. **Presentation Layer**: Frontend UI components\n2. **Application Layer**: Business logic and API endpoints\n3. **Data Layer**: Database interactions and data models\n\n"
        
        if 'requirements' in sections:
            content += "## Requirements\n\n### Functional Requirements\n- User authentication and authorization\n- CRUD operations for main resources\n- Search and filter functionality\n- Export data in multiple formats\n\n### Non-Functional Requirements\n- Response time < 200ms for API calls\n- 99.9% uptime\n- Support for 1000+ concurrent users\n\n"
        
        if 'tech-stack' in sections:
            content += "## Technology Stack\n\n- **Frontend**: React, Redux, Material UI\n- **Backend**: Flask/Python\n- **Database**: PostgreSQL\n- **Deployment**: Docker, Kubernetes\n- **CI/CD**: GitHub Actions\n\n"
        
        return jsonify({
            'content': content,
            'format': output_format,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/tests', methods=['POST'])
def create_tests():
    """Generate test cases for code"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'python')
    framework = data.get('framework', 'pytest')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        # Use the AI service to generate tests
        tests = generate_tests(code, language, framework)
        return jsonify({'tests': tests})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/generate-tests', methods=['POST'])
def generate_automated_tests():
    """Generate automated test cases for code"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'javascript')
    framework = data.get('framework', 'jest')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    try:
        # In a real implementation, this would call an AI service
        # For now, we'll generate a mock response based on the language and framework
        
        if language == 'javascript':
            if framework == 'jest':
                tests = """// Generated Jest tests
const { functionName } = require('./yourModule');

describe('functionName', () => {
  test('should handle basic input correctly', () => {
    expect(functionName('test')).toBe('expected result');
  });

  test('should handle edge cases', () => {
    expect(functionName('')).toBe('');
    expect(functionName(null)).toBeNull();
  });

  test('should throw error for invalid input', () => {
    expect(() => functionName(undefined)).toThrow();
  });
});"""
            else:  # mocha
                tests = """// Generated Mocha tests
const assert = require('assert');
const { functionName } = require('./yourModule');

describe('functionName', function() {
  it('should handle basic input correctly', function() {
    assert.strictEqual(functionName('test'), 'expected result');
  });

  it('should handle edge cases', function() {
    assert.strictEqual(functionName(''), '');
    assert.strictEqual(functionName(null), null);
  });

  it('should throw error for invalid input', function() {
    assert.throws(() => functionName(undefined));
  });
});"""
        elif language == 'python':
            if framework == 'pytest':
                tests = """# Generated pytest tests
import pytest
from your_module import function_name

def test_basic_functionality():
    assert function_name("test") == "expected result"

def test_edge_cases():
    assert function_name("") == ""
    assert function_name(None) is None

def test_invalid_input():
    with pytest.raises(Exception):
        function_name(undefined_variable)
"""
            else:  # unittest
                tests = """# Generated unittest tests
import unittest
from your_module import function_name

class TestFunctionName(unittest.TestCase):
    def test_basic_functionality(self):
        self.assertEqual(function_name("test"), "expected result")

    def test_edge_cases(self):
        self.assertEqual(function_name(""), "")
        self.assertIsNone(function_name(None))

    def test_invalid_input(self):
        with self.assertRaises(Exception):
            function_name(undefined_variable)

if __name__ == '__main__':
    unittest.main()
"""
        else:  # Default to Java JUnit
            tests = """// Generated JUnit tests
import org.junit.Test;
import static org.junit.Assert.*;

public class FunctionNameTest {
    @Test
    public void testBasicFunctionality() {
        assertEquals("expected result", FunctionName.execute("test"));
    }

    @Test
    public void testEdgeCases() {
        assertEquals("", FunctionName.execute(""));
        assertNull(FunctionName.execute(null));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testInvalidInput() {
        FunctionName.execute(undefined);
    }
}
"""
        
        return jsonify({
            'tests': tests,
            'language': language,
            'framework': framework,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
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
