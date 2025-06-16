# AetherCode - Intelligent Code Refinement

AetherCode is a modern, clean, and intuitive web application designed for code analysis, review, and execution. With its sleek interface and powerful features, it provides developers with an efficient environment for writing, testing, and improving their code.

## Features

### Code Editor
- Syntax highlighting for multiple programming languages
- Code execution with real-time output display
- Language-specific formatting
- Code folding and bracket matching
- Keyboard shortcuts
- Enhanced drag-and-drop file upload functionality

### AI Code Reviewer
- Intelligent code analysis and review
- Interactive chat interface for coding assistance
- Project-level analysis for multiple files
- Downloadable code review reports

## Project Structure

The project follows a modular Flask application structure:

```
AetherCode/
├── app/                    # Main application package
│   ├── __init__.py         # Flask app factory
│   ├── config/             # Configuration modules
│   │   ├── __init__.py
│   │   ├── language_config.py
│   │   └── analysis_patterns.py
│   ├── routes/             # Route handlers
│   │   ├── __init__.py
│   │   ├── main_routes.py  # Main routes
│   │   └── api_routes.py   # API endpoints
│   ├── services/           # Business logic
│   │   ├── __init__.py
│   │   ├── code_executor.py
│   │   ├── code_analyzer.py
│   │   ├── code_reviewer.py
│   │   ├── chat_service.py
│   │   ├── file_handler.py
│   │   └── ai_service.py
│   ├── templates/          # HTML templates
│   │   └── index.html
│   └── utils/              # Utility functions
│       ├── __init__.py
│       ├── error_handler.py
│       └── logger.py
├── static/                 # Static assets
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── script.js
│   │   └── animations.js
│   └── images/
├── logs/                   # Application logs
├── run.py                  # Application entry point
└── README.md               # Project documentation
```

### Coming Soon
- Technical specification generation
- Automated test case generation

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript, CodeMirror
- **Backend**: Flask (Python)
- **AI Integration**: OpenAI API for intelligent code review and assistance

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Start the Flask backend:
   ```
   python app.py
   ```
4. Open `index.html` in your web browser or serve it using a local server

## API Endpoints

The application connects to a Flask backend with the following endpoints:

- `/api/execute` - Execute code and return output
- `/api/chat` - Chat with AI assistant
- `/api/review` - Submit code for AI review
- `/api/upload` - Upload files for analysis

## User Interface

The UI features a clean, modern, minimalistic, and aesthetic design with:
- Sophisticated, soft color palette with muted tones
- Subtle gradients and judicious use of accent colors
- Smooth, purposeful animations
- Elegant, intuitive tabbed navigation system
- Clear visual hierarchy and ample whitespace

## License

MIT
