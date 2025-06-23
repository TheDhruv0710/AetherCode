from flask import Flask, render_template
from dotenv import load_dotenv
from config import DEBUG, OPENAI_API_KEY

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configure app
app.config['DEBUG'] = DEBUG
app.config['SECRET_KEY'] = 'aethercode-secret-key'  # Change this in production

# Check if OpenAI API key is configured
if not OPENAI_API_KEY:
    print("\n" + "*" * 80)
    print("WARNING: OpenAI API key is not set. The application will use mock data.")
    print("To use the OpenAI API, create a .env file with your OPENAI_API_KEY.")
    print("See .env.example for reference.")
    print("*" * 80 + "\n")

# Import and register blueprints
from routes import main_routes
app.register_blueprint(main_routes)

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=5000)
