import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Azure OpenAI API configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_API_BASE = os.getenv('OPENAI_API_BASE')  # Azure OpenAI API base URL
OPENAI_API_TYPE = 'azure'  # Set API type to Azure
OPENAI_API_VERSION = os.getenv('OPENAI_API_VERSION', '2023-05-15')  # Azure OpenAI API version
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')  # Default to GPT-3.5 Turbo

# Repository settings
TEMP_REPO_DIR = os.getenv('TEMP_REPO_DIR', '/tmp')

# Flask configuration
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
