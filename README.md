# AetherCode - AI-Powered Code Review Platform

AetherCode is an intelligent code review application that replaces traditional code review meetings with an AI interviewer. It analyzes GitHub repositories, conducts interactive discussions, and generates comprehensive technical documentation in real-time.

## Features

- **Repository Analysis**: Clone and analyze public GitHub repositories
- **AI-Powered Chat**: Interactive discussions about your codebase with Azure OpenAI
- **Technical Specifications**: Auto-generated technical documentation
- **Code Health Reports**: Comprehensive code quality analysis
- **Meeting Minutes**: Automated documentation of review sessions
- **Insights Generation**: AI-driven insights and recommendations
- **File Explorer**: Browse repository structure with syntax highlighting
- **Export Reports**: Generate and export comprehensive reports

## Tech Stack

### Frontend
- **HTML5/CSS3/JavaScript**: Modern vanilla web technologies
- **Inter Font**: Clean, professional typography
- **Violet Theme**: Modern dark theme with violet accents

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: Database ORM
- **Azure OpenAI**: AI-powered analysis and chat
- **GitPython**: Git repository operations
- **SQLite**: Local database storage

## Quick Start

### Prerequisites
- Python 3.8+
- Git
- Azure OpenAI API access

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Aether2
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your Azure OpenAI credentials:
   ```env
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | `abc123...` |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | `https://myresource.openai.azure.com/` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Deployment name in Azure | `gpt-4` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `AZURE_OPENAI_API_VERSION` | API version | `2024-02-15-preview` |
| `FLASK_SECRET_KEY` | Flask secret key | Auto-generated |
| `FLASK_DEBUG` | Debug mode | `False` |
| `FLASK_HOST` | Server host | `127.0.0.1` |
| `FLASK_PORT` | Server port | `5000` |
| `SQLALCHEMY_DATABASE_URI` | Database URI | `sqlite:///aethercode.db` |

## Project Structure

```
Aether2/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── index.html                 # Main HTML file
├── static/
│   ├── css/
│   │   ├── style.css          # Main styles
│   │   └── file-explorer.css  # File explorer styles
│   └── js/
│       └── script.js          # Frontend JavaScript
├── services/
│   ├── ai_service.py          # Azure OpenAI integration
│   └── repo_service.py        # Git repository operations
├── blueprints/
│   ├── repo_bp.py             # Repository API endpoints
│   └── ai_bp.py               # AI chat and reports API
├── temp_repos/                # Temporary repository storage
└── logs/                      # Application logs
```

## API Endpoints

### Repository Management
- `POST /api/repo/analyze` - Analyze a GitHub repository
- `GET /api/repo/<project_id>/file` - Get file content
- `GET /api/repo/<project_id>/structure` - Get repository structure
- `GET /api/repo/<project_id>/info` - Get project information
- `DELETE /api/repo/<project_id>` - Delete project

### AI Services
- `POST /api/ai/chat` - Chat with AI about the repository
- `GET /api/ai/reports/<project_id>` - Generate comprehensive reports
- `GET /api/ai/conversation/<project_id>` - Get conversation history
- `POST /api/ai/regenerate-tech-spec/<project_id>` - Regenerate technical specification
- `GET /api/ai/status` - Check AI service status

### Health Check
- `GET /health` - Application health status

## Usage

1. **Start Analysis**: Enter a public GitHub repository URL on the landing page
2. **Explore Code**: Use the file explorer to browse the repository structure
3. **Chat with AI**: Ask questions about the codebase in the chat interface
4. **Review Reports**: Generate and view technical specifications, code health reports, and insights
5. **Export Results**: Download comprehensive reports for documentation

## Security Features

- **Public Repositories Only**: No authentication required for GitHub access
- **Environment Variables**: Secure configuration management
- **Input Validation**: Comprehensive request validation
- **Error Handling**: Robust error management and logging
- **CORS Protection**: Configured cross-origin resource sharing

## Troubleshooting

### Common Issues

1. **Azure OpenAI Connection Errors**
   - Verify your API key and endpoint are correct
   - Check your Azure OpenAI deployment is active
   - Ensure you have sufficient quota

2. **Repository Clone Failures**
   - Verify the GitHub URL is public and accessible
   - Check your internet connection
   - Ensure sufficient disk space

3. **Database Issues**
   - Check file permissions for SQLite database
   - Verify the database directory is writable

### Logs
Check `logs/aethercode.log` for detailed error information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request




class GenAi:
    def __init__(self, link_data):
        model_name = os.getenv("model_name")
        deployment_name = os.getenv("deployment_name")
        print(link_data)

        os.environ['OPENAI_API_TYPE'] = os.getenv("api_type")
        os.environ['AZURE_OPENAI_ENDPOINT'] = os.getenv("api_base")
        os.environ['OPENAI_API_KEY'] = os.getenv("api_key")
        os.environ['OPENAI_API_VERSION'] = os.getenv("api_version")
        self.model = AzureChatOpenAI(
            deployment_name=deployment_name,
            model_name=model_name
        )
        self.link_data = link_data
        print(f"prompt_template: {os.getenv('prompt_template')}")
        self.prompt_template = PromptTemplate(
            input_variables=["link_data"],
            template=os.getenv("prompt_template"),
        )

        self.chain = self.prompt_template | self.model

    def generate_response(self, message):
        prompt_input = {
            "link_data": self.link_data,
            "message": message
        }
        response = self.chain.invoke(prompt_input)
        return response.content



## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Azure OpenAI for AI capabilities
- Flask community for the excellent framework
- GitHub for repository hosting and API access
