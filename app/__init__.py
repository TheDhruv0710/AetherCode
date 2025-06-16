"""
AetherCode Application Package
"""
from flask import Flask
from flask_cors import CORS
import os

def create_app(config=None):
    """Create and configure the Flask application"""
    # Initialize Flask app with static files in static folder
    app = Flask(__name__, 
                static_url_path='/static', 
                static_folder='../static',
                template_folder='templates')
    
    # Enable CORS for all routes
    CORS(app)
    
    # Configure static file caching (disable during development)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
    # Set default configuration
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_key_for_development_only'),
        DEBUG=True
    )
    
    # Apply configuration overrides
    if config:
        app.config.update(config)
    
    # Register error handlers
    from app.utils.error_handler import register_error_handlers
    register_error_handlers(app)
    
    # Set up logging
    from app.utils.logger import setup_logger
    setup_logger(app)
    
    # Register blueprints
    from app.routes.main_routes import main_bp
    from app.routes.api_routes import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    app.logger.info('AetherCode application initialized')
    
    return app
