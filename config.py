import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')  # Default to GPT-4 if not specified

# Repository settings
TEMP_REPO_DIR = os.getenv('TEMP_REPO_DIR', '/tmp')

# Flask configuration
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
