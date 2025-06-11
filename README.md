# AetherCode - AI Code Reviewer

A modern, aesthetic web application for AI-powered code reviews with advanced code editing capabilities.

## Overview

AetherCode is a sleek, visually stunning web interface with an integrated Flask backend for AI code reviews. The application features a modern UI with a dark theme, animated background, responsive layout, and a powerful CodeMirror editor for syntax highlighting and code formatting.

## Features

- **Advanced Code Editor**: CodeMirror integration with syntax highlighting for multiple languages
- **Code Formatting**: Language-specific code formatting with a dedicated format button
- **Code Folding**: Collapsible code sections for better readability
- **Bracket Matching**: Automatic highlighting of matching brackets
- **File Upload**: Support for both single file and project/archive uploads with drag-and-drop
- **AI Chat Interface**: Interactive chat with the AI code reviewer
- **Code Analysis**: Automated code quality assessment and suggestions
- **Responsive Design**: Adapts seamlessly to various screen sizes
- **Animated Background**: Subtle floating particles animation for visual appeal
- **Typing Animation**: Dynamic text animation in the header

## Project Structure

```
AetherCode/
├── index.html          # Main HTML file
├── css/
│   └── styles.css      # Styling for the application
├── js/
│   ├── animations.js   # Background and typing animations
│   ├── editor.js       # CodeMirror editor functionality
│   └── main.js         # Core application logic
├── backend/            # Flask backend
│   ├── app.py          # Main Flask application
│   ├── services/       # Backend services
│   │   ├── ai_service.py     # AI chat and code analysis
│   │   └── code_analyzer.py  # Code quality analysis
│   ├── requirements.txt # Python dependencies
│   └── .env            # Environment variables
└── README.md           # Project documentation
```

## Getting Started

### Frontend
1. Clone this repository
2. Open `index.html` in your browser or use a simple HTTP server:
   ```
   python -m http.server 8000
   ```
3. Access the application at `http://localhost:8000`

### Backend
1. Navigate to the backend directory:
   ```
   cd backend
   ```
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key in the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Start the Flask server:
   ```
   python app.py
   ```
5. The backend will be available at `http://localhost:5000`

## API Endpoints

- **POST /api/analyze**: Analyze code and provide feedback
- **POST /api/chat**: Process chat messages with AI
- **POST /api/upload**: Handle single file uploads
- **POST /api/project**: Handle multiple file/project uploads

## Technologies Used

### Frontend
- HTML5
- CSS3 (with modern animations and flexbox layout)
- Vanilla JavaScript (ES6+)
- CodeMirror 5.x (code editor with syntax highlighting)
- js-beautify (code formatting)
- Font Awesome for icons
- Google Fonts for typography

### Backend
- Flask (Python web framework)
- Flask-CORS (Cross-Origin Resource Sharing)
- OpenAI API (for AI code analysis and chat)
- Python-dotenv (environment variable management)

## Browser Compatibility

The application is designed to work with modern browsers including:
- Chrome
- Firefox
- Safari
- Edge

## License

MIT
