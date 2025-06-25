import os
import logging
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from models import db
from blueprints.repo_bp import repo_bp
from blueprints.ai_bp import ai_bp

# Load environment variables from .env file
load_dotenv()

def setup_logging():
    """Configure logging for the application"""
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure file handler
    file_handler = logging.FileHandler(os.path.join(log_dir, 'aethercode.log'))
    file_handler.setLevel(logging.INFO)
    
    # Configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    logging.info("Logging configured successfully")

def validate_environment():
    """Validate required environment variables"""
    required_vars = [
        'AZURE_OPENAI_API_KEY',
        'AZURE_OPENAI_ENDPOINT',
        'AZURE_OPENAI_DEPLOYMENT_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    logging.info("Environment variables validated successfully")

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure app from environment variables
    app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'aethercode-dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'SQLALCHEMY_DATABASE_URI', 
        f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'aethercode.db')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }

    # Setup logging
    setup_logging()
    
    # Validate environment
    try:
        validate_environment()
    except ValueError as e:
        logging.error(f"Environment validation failed: {e}")
        raise

    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(repo_bp, url_prefix='/api/repo')
    app.register_blueprint(ai_bp, url_prefix='/api/ai')

    # Create database tables
    with app.app_context():
        try:
            db.create_all()
            logging.info("Database tables created successfully")
        except Exception as e:
            logging.error(f"Error creating database tables: {e}")
            raise

    @app.route('/')
    def serve_index():
        """Serve the main HTML file"""
        return send_from_directory('.', 'index.html')

    @app.route('/static/<path:path>')
    def serve_static(path):
        """Serve static files"""
        return send_from_directory('static', path)

    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        try:
            # Test database connection
            db.session.execute(db.text('SELECT 1'))
            db.session.commit()
            
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'timestamp': str(db.func.now())
            })
        except Exception as e:
            logging.error(f"Health check failed: {e}")
            return jsonify({
                'status': 'unhealthy',
                'error': str(e)
            }), 500

    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors"""
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors"""
        logging.error(f"Internal server error: {error}")
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(Exception)
    def handle_exception(e):
        """Handle unexpected exceptions"""
        logging.error(f"Unhandled exception: {e}", exc_info=True)
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occurred'}), 500

    # Log startup information
    logging.info("AetherCode application created successfully")
    logging.info(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    logging.info(f"Azure OpenAI Endpoint: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
    logging.info(f"Azure OpenAI Deployment: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")

    return app

if __name__ == '__main__':
    try:
        app = create_app()
        
        # Get configuration from environment
        debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        port = int(os.getenv('FLASK_PORT', 5000))
        host = os.getenv('FLASK_HOST', '127.0.0.1')
        
        logging.info(f"Starting AetherCode server on {host}:{port} (debug={debug_mode})")
        
        app.run(
            debug=debug_mode,
            host=host,
            port=port,
            use_reloader=False  # Disable reloader to prevent issues with file operations
        )
        
    except Exception as e:
        logging.error(f"Failed to start application: {e}")
        raise
