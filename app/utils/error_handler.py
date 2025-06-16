"""
Error handling utilities for AetherCode application
"""
from flask import jsonify

class APIError(Exception):
    """Base class for API errors"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """Convert error to dictionary for JSON response"""
        result = dict(self.payload or ())
        result['error'] = self.message
        return result

def handle_api_error(error):
    """Handle API errors and return appropriate response"""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def register_error_handlers(app):
    """Register error handlers with Flask app"""
    app.register_error_handler(APIError, handle_api_error)
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
