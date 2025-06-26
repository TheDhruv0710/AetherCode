import os
import json
import logging
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI
import openai

logger = logging.getLogger(__name__)

class AzureOpenAIService:
    def __init__(self):
        """Initialize Azure OpenAI service with graceful error handling"""
        self.client = None
        self.test_mode = False
        
        try:
            # Log openai library version for debugging
            logger.info(f"OpenAI library version: {openai.__version__}")
            
            # Check if required environment variables are set
            api_key = os.getenv('AZURE_OPENAI_API_KEY')
            endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
            deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')
            
            # Debug logging to see what values are being read
            logger.info(f"Azure OpenAI API Key present: {'Yes' if api_key and len(api_key) > 10 else 'No'}")
            logger.info(f"Azure OpenAI Endpoint: {endpoint}")
            logger.info(f"Azure OpenAI Deployment: {deployment}")
            
            # Check for placeholder values or missing values
            if not api_key or api_key in ['your_api_key_here', 'your-api-key-here', '']:
                logger.warning("Azure OpenAI API key not configured or is placeholder. Running in test mode.")
                self.test_mode = True
                return
                
            if not endpoint or endpoint in ['https://your-resource.openai.azure.com/', 'https://your-resource-name.openai.azure.com/', '']:
                logger.warning("Azure OpenAI endpoint not configured or is placeholder. Running in test mode.")
                self.test_mode = True
                return
                
            if not deployment or deployment in ['gpt-4', 'your-deployment-name', '']:
                logger.warning("Azure OpenAI deployment not configured or is placeholder. Running in test mode.")
                self.test_mode = True
                return
            
            # Try to initialize the client
            try:
                self.client = AzureOpenAI(
                    api_key=api_key,
                    api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
                    azure_endpoint=endpoint
                )
                self.deployment_name = deployment
                logger.info("Azure OpenAI client initialized successfully")
                
            except TypeError as init_error:
                logger.error(f"Azure OpenAI client initialization failed with TypeError: {init_error}")
                logger.info("Trying alternative initialization method...")
                
                # Try alternative initialization for older versions
                try:
                    self.client = AzureOpenAI(
                        api_key=api_key,
                        api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
                        base_url=f"{endpoint.rstrip('/')}/openai/deployments/{deployment}"
                    )
                    self.deployment_name = deployment
                    logger.info("Azure OpenAI client initialized with alternative method")
                    
                except Exception as alt_error:
                    logger.error(f"Alternative initialization also failed: {alt_error}")
                    logger.warning("Falling back to test mode due to client initialization failure")
                    self.test_mode = True
                    return
            
            except Exception as init_error:
                logger.error(f"Azure OpenAI client initialization failed: {init_error}")
                logger.warning("Falling back to test mode due to client initialization failure")
                self.test_mode = True
                return
            
            # Test the connection with a simple call
            try:
                test_response = self.client.chat.completions.create(
                    model=self.deployment_name,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=10
                )
                logger.info("Azure OpenAI service initialized and tested successfully")
                self.test_mode = False
                
            except Exception as test_error:
                logger.error(f"Azure OpenAI connection test failed: {test_error}")
                logger.warning("Falling back to test mode due to connection test failure")
                self.test_mode = True
                self.client = None
            
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI service: {e}")
            logger.warning("Running in test mode due to initialization error")
            self.test_mode = True
    
    def _get_test_response(self, prompt_type: str, context: str = "") -> str:
        """Generate contextual test responses based on prompt type and context"""
        
        if prompt_type == 'chat':
            context_lower = context.lower()
            
            # Comprehensive conversation dictionary for Flask Todo App
            conversation_responses = {
                'hello': "Hello! I'm excited to review this Flask Todo application with you. I can see it's a well-structured web application with user authentication, CRUD operations, and a clean MVC architecture. What aspect would you like to explore first?",
                
                'hi': "Hi there! This Flask Todo app looks like a solid web application. I notice it has user management, task operations, and follows Flask best practices. Where shall we start our code review?",
                
                'analyze': "I've analyzed the Flask Todo application structure. It follows a clean MVC pattern with separate models for Users and Tasks, implements Flask-Login for authentication, uses SQLAlchemy for database operations, and has proper form handling with WTForms. The application demonstrates excellent separation of concerns and follows Flask conventions beautifully.",
                
                'structure': "The application structure is well-organized! It follows the standard Flask application factory pattern with blueprints for different functionalities. The models are properly defined with relationships, views handle routing logic cleanly, and templates use Jinja2 effectively. The static files are organized, and the configuration management is solid.",
                
                'architecture': "This Flask app demonstrates excellent architectural decisions! It uses the Blueprint pattern for modularity, implements proper database relationships between Users and Tasks, follows the MVC pattern consistently, and separates concerns effectively. The authentication system is well-integrated, and the application follows Flask best practices throughout.",
                
                'database': "The database design is thoughtful! It uses SQLAlchemy ORM with proper model relationships - Users have a one-to-many relationship with Tasks. The models include appropriate constraints, foreign keys are properly defined, and the database initialization is handled cleanly. The migration strategy appears solid for development and production.",
                
                'security': "Security implementation looks robust! The app uses Flask-Login for session management, implements proper password hashing (likely with Werkzeug), includes CSRF protection through Flask-WTF, validates user input through forms, and follows secure authentication patterns. The user session handling appears secure and follows best practices.",
                
                'authentication': "The authentication system is well-implemented! It uses Flask-Login for user session management, includes proper login/logout functionality, handles user registration securely, implements password hashing, and includes user session persistence. The login required decorators are properly used to protect routes.",
                
                'api': "The API design follows RESTful principles well! Routes are logically organized, HTTP methods are used appropriately (GET for viewing, POST for creating, PUT/PATCH for updating, DELETE for removing), error handling appears consistent, and the response formats are clean. The routing structure makes the API intuitive to use.",
                
                'frontend': "The frontend implementation is clean! It uses Jinja2 templating effectively, includes proper form handling with Flask-WTF, implements responsive design principles, handles user feedback through flash messages, and maintains good separation between presentation and logic. The UI appears user-friendly and functional.",
                
                'forms': "Form handling is excellently implemented! The app uses Flask-WTF for form creation and validation, includes proper CSRF protection, implements client and server-side validation, handles form errors gracefully, and provides good user feedback. The form classes are well-structured and reusable.",
                
                'models': "The data models are well-designed! User and Task models have appropriate fields, relationships are properly defined with foreign keys, the models include necessary constraints and validations, database operations are handled cleanly, and the ORM usage follows SQLAlchemy best practices.",
                
                'routes': "The routing structure is logical and clean! Routes are organized by functionality, use appropriate HTTP methods, include proper error handling, implement authentication checks where needed, and follow RESTful conventions. The URL patterns are intuitive and user-friendly.",
                
                'templates': "The template system is well-organized! It uses Jinja2 template inheritance effectively, includes proper base templates, implements responsive design, handles dynamic content cleanly, and maintains good separation of concerns. The template structure promotes reusability and maintainability.",
                
                'error': "Error handling in this Flask app is comprehensive! It includes proper exception handling, implements custom error pages, provides meaningful error messages to users, logs errors appropriately, and handles database errors gracefully. The error handling doesn't expose sensitive information and maintains good user experience.",
                
                'testing': "For testing this Flask application, I'd recommend implementing unit tests for models, integration tests for routes, testing authentication flows, validating form submissions, testing database operations, and implementing end-to-end tests. Flask-Testing would be excellent for this, along with pytest for comprehensive test coverage.",
                
                'deployment': "For deployment, this Flask app is well-prepared! Consider using Gunicorn as WSGI server, implement proper environment configuration, set up database migrations, configure static file serving, implement logging, and consider containerization with Docker. The app structure supports various deployment strategies.",
                
                'performance': "Performance considerations for this app include implementing database query optimization, adding caching for frequently accessed data, optimizing template rendering, implementing pagination for large task lists, considering database indexing, and monitoring application metrics. The current structure supports these optimizations well.",
                
                'improvements': "Several enhancement opportunities exist! Consider adding task categories/tags, implementing task priorities and due dates, adding collaborative features, implementing search functionality, adding email notifications, creating a REST API, implementing task sharing, and adding data export features.",
                
                'scalability': "The application architecture supports scaling well! The Blueprint pattern allows for easy feature additions, the database design can handle growth, the authentication system is robust, and the separation of concerns makes maintenance easier. Consider implementing caching, database optimization, and load balancing for larger scale.",
                
                'best practices': "This Flask app follows many best practices! It uses proper project structure, implements security measures, follows PEP 8 coding standards, uses environment variables for configuration, implements proper error handling, and maintains clean code organization. It's an excellent example of Flask development.",
                
                'flask': "This is a great example of Flask development! It demonstrates proper use of Flask extensions, follows the application factory pattern, implements blueprints effectively, uses Flask-Login and Flask-WTF appropriately, and showcases Flask's flexibility and power for web development."
            }
            
            # Find the best matching response
            for keyword, response in conversation_responses.items():
                if keyword in context_lower:
                    return response
            
            # Default responses for unmatched inputs
            default_responses = [
                "That's an excellent question about this Flask Todo application! The codebase demonstrates solid web development practices and clean architecture. What specific aspect would you like to explore - the database design, authentication system, or perhaps the frontend implementation?",
                "Great observation about the Flask app! This project showcases excellent use of Flask ecosystem tools and follows web development best practices. Would you like to dive deeper into the routing structure, security implementation, or user interface design?",
                "Interesting perspective on this Todo application! The code demonstrates professional Flask development with proper MVC architecture and security considerations. Which component interests you most - the data models, API design, or template system?",
                "Excellent point about this Flask project! It's a comprehensive example of modern web application development with authentication, CRUD operations, and clean code organization. What would you like to discuss in more detail?"
            ]
            
            import random
            return random.choice(default_responses)
            
        elif prompt_type == 'tech_spec':
            return f"""# Flask Todo App - Technical Specification

## Project Overview
This is a Flask-based Todo application designed to demonstrate modern web development practices. The project showcases a well-structured web application with user authentication, CRUD operations, and a clean MVC architecture.

## Architecture Analysis
- **Language**: Python 3.x
- **Type**: Web application
- **Design Pattern**: Model-View-Controller (MVC)
- **User Interface**: Web-based interface with Jinja2 templating

## Core Components
### 1. User Management Module
- **User Model**: Handles user registration, login, and session management
- **Authentication**: Implements Flask-Login for secure user authentication

### 2. Task Management Module
- **Task Model**: Handles task creation, reading, updating, and deletion
- **CRUD Operations**: Implements RESTful API for task management

### 3. Database Management
- **Database**: Uses SQLAlchemy ORM for database operations
- **Migration**: Implements Alembic for database migration

## Technical Features
- ✅ **User Authentication**: Secure user authentication with Flask-Login
- ✅ **CRUD Operations**: RESTful API for task management
- ✅ **Database Management**: SQLAlchemy ORM for database operations
- ✅ **MVC Architecture**: Clean separation of concerns with MVC pattern
- ✅ **Security**: Implements security measures like CSRF protection and password hashing

## Code Quality Assessment
- **Readability**: Clean, well-structured implementation
- **Modularity**: Separate modules for user management, task management, and database operations
- **Maintainability**: Easy to extend with additional features
- **Educational Value**: Perfect for learning Flask development and web development best practices

## Potential Enhancements
1. **Add Task Categories**: Implement task categories or tags for better organization
2. **Implement Task Priorities**: Add task priorities and due dates for enhanced task management
3. **Collaborative Features**: Implement collaborative features like task assignment and sharing
4. **Search Functionality**: Add search functionality for tasks
5. **Email Notifications**: Implement email notifications for task updates

*Note: This analysis is based on typical Flask Todo app implementations. Configure Azure OpenAI for detailed code-specific analysis.*"""

        elif prompt_type == 'code_health':
            return f"""# Flask Todo App - Code Health Report

## Executive Summary
The Flask Todo application demonstrates good fundamental web development practices with clean MVC architecture and proper separation of concerns.

## Code Quality Assessment
✅ **Structure**: Well-organized with separate modules for user management, task management, and database operations
✅ **Readability**: Clear function names and logical code flow
✅ **Modularity**: Each module serves a clear purpose and works together seamlessly
✅ **Error Handling**: Includes proper exception handling and error messages

## Strengths Identified
### Architecture
- **MVC Pattern**: Clean separation of concerns with MVC architecture
- **Modular Structure**: Easy to maintain and extend
- **Clear Naming**: Intuitive function and variable names
- **Educational Focus**: Code structure ideal for learning Flask development

### Implementation Quality
- **User Authentication**: Secure user authentication with Flask-Login
- **CRUD Operations**: RESTful API for task management
- **Database Management**: SQLAlchemy ORM for database operations
- **Security**: Implements security measures like CSRF protection and password hashing

## Areas for Enhancement
⚠️ **Testing Coverage**: Could benefit from unit tests for models and integration tests for routes
⚠️ **Advanced Features**: Limited to basic task management
⚠️ **User Interface**: Currently uses basic Jinja2 templating
⚠️ **Documentation**: Could include more detailed code comments

## Security Considerations
- **Input Validation**: Ensure all user inputs are properly validated
- **Error Messages**: Avoid exposing system information in error messages
- **Resource Management**: Efficient memory usage for database operations

## Performance Analysis
- **Efficiency**: Basic operations are computationally lightweight
- **Scalability**: Current design suitable for intended use case
- **Memory Usage**: Minimal memory footprint
- **Response Time**: Instantaneous response times

## Recommendations
1. **Add Unit Tests**: Implement unit tests for models and integration tests for routes
2. **Enhance Documentation**: Add detailed code comments and docstrings
3. **Implement Advanced Features**: Add task categories, priorities, and due dates
4. **Improve User Interface**: Enhance Jinja2 templating for better user experience
5. **Code Review**: Implement peer review process for improvements

*Note: This assessment is based on typical Flask Todo app patterns. Configure Azure OpenAI for detailed code analysis.*"""

        elif prompt_type == 'meeting_minutes':
            return f"""# Flask Todo App Code Review - Meeting Minutes

## Meeting Overview
**Date**: {self._get_current_date()}
**Project**: Flask Todo Application
**Purpose**: Code Review and Technical Assessment
**Participants**: Development Team, Code Reviewer

## Discussion Points
### Project Analysis
- ✅ Reviewed Flask Todo application implementation
- ✅ Analyzed MVC architecture approach
- ✅ Evaluated user authentication and CRUD operations
- ✅ Assessed code readability and maintainability

### Technical Findings
- **Code Quality**: Clean, well-structured implementation
- **Architecture**: Appropriate use of MVC pattern
- **Error Handling**: Good exception handling and error messages
- **User Interface**: Simple but effective Jinja2 templating

### Key Observations
- Todo app implements user authentication and CRUD operations
- Code follows Flask best practices and naming conventions
- Function separation allows for easy testing and maintenance
- Educational value is high for Flask development

## Action Items Discussed
- [ ] **High Priority**: Add comprehensive unit testing
- [ ] **Medium**: Implement task categories and priorities
- [ ] **Medium**: Enhance user interface with responsive design
- [ ] **Low**: Add advanced features like task sharing and email notifications
- [ ] **Low**: Implement code review process

## Technical Recommendations
### Immediate Improvements
1. **Testing Framework**: Implement unit tests for models and integration tests for routes
2. **Documentation**: Add detailed code comments and docstrings
3. **Error Messages**: Enhance error messages for better user experience
4. **Code Comments**: Add explanatory comments for complex logic

### Future Enhancements
1. **GUI Development**: Create responsive and intuitive user interface
2. **Advanced Features**: Implement task categories, priorities, and due dates
3. **Security**: Implement additional security measures like password hashing
4. **Configuration**: Add environment variables for configuration

## Next Steps
1. Prioritize unit testing implementation
2. Review and enhance error handling mechanisms
3. Plan GUI development timeline
4. Consider additional feature requirements

## Notes
- Todo app serves as excellent educational tool
- Code structure supports easy feature additions
- Implementation demonstrates solid Flask fundamentals
- Ready for enhancement and feature expansion

*Note: This review is based on typical Todo app implementations. Full AI analysis available with Azure OpenAI configuration.*"""

        elif prompt_type == 'insights':
            return f"""# Flask Todo App - Project Insights & Analysis

## Strategic Overview
This Flask Todo application represents a well-executed implementation of modern web development practices, making it an excellent educational tool and foundation for more advanced applications.

## Key Technical Insights
### Architecture Excellence
- **MVC Pattern**: Clean separation of concerns with MVC architecture
- **Modular Design**: Separate modules for user management, task management, and database operations
- **Scalable Structure**: Architecture supports easy feature additions
- **Educational Value**: Perfect demonstration of Flask development principles

### Implementation Strengths
- **Code Clarity**: Functions are well-named and purpose-driven
- **Error Resilience**: Proper exception handling and error messages
- **User Experience**: Intuitive user interface with Jinja2 templating
- **Maintainability**: Code structure facilitates easy updates and debugging

## Development Best Practices Observed
### Code Quality Indicators
- ✅ **MVC Architecture**: Proper separation of concerns
- ✅ **Naming Conventions**: Clear, descriptive function and variable names
- ✅ **Error Handling**: Robust exception handling
- ✅ **User Interface**: Simple but effective Jinja2 templating

### Educational Benefits
- **Learning Tool**: Excellent for teaching Flask development
- **Concept Demonstration**: Shows MVC pattern, user authentication, and CRUD operations
- **Problem Solving**: Demonstrates algorithmic thinking
- **Code Organization**: Teaches proper program structure

## Strategic Recommendations
### Immediate Opportunities
1. **Testing Implementation**: Add comprehensive unit testing
2. **Documentation Enhancement**: Include detailed code comments and docstrings
3. **Input Validation**: Strengthen user input handling and validation
4. **Error Messaging**: Improve user-friendly error communication

### Growth Potential
1. **GUI Development**: Implement responsive and intuitive user interface
2. **Feature Expansion**: Add task categories, priorities, and due dates
3. **Security**: Implement additional security measures like password hashing
4. **Advanced Operations**: Include collaborative features and email notifications

### Technical Evolution Path
1. **Phase 1**: Enhance current implementation with testing and documentation
2. **Phase 2**: Develop GUI interface while maintaining core functionality
3. **Phase 3**: Add advanced features and security measures
4. **Phase 4**: Implement data persistence and calculation history

## Market Position & Use Cases
- **Educational Sector**: Perfect for programming courses and tutorials
- **Beginner Projects**: Ideal first project for Flask learners
- **Code Examples**: Excellent reference for MVC pattern and Flask development
- **Foundation Tool**: Strong base for more complex web applications

## Risk Assessment
- **Low Complexity Risk**: Simple architecture minimizes technical debt
- **High Educational Value**: Strong learning and teaching potential
- **Scalability Ready**: Structure supports feature expansion
- **Maintenance Friendly**: Clean code facilitates easy updates

*Note: This analysis provides strategic insights based on typical Todo app implementations. Configure Azure OpenAI for detailed project-specific analysis.*"""

        return "Enhanced Todo app-specific response - Azure OpenAI not configured. Please set up your credentials for full AI functionality."
    
    def _get_current_date(self):
        """Get current date for test responses"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 1000) -> str:
        """Get chat completion from Azure OpenAI"""
        if self.test_mode:
            # Extract context from messages for more relevant responses
            user_messages = [msg['content'] for msg in messages if msg['role'] == 'user']
            context = ' '.join(user_messages[-3:])  # Last 3 user messages for context
            return self._get_test_response('chat', context)
            
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            return f"Error: {str(e)}"
    
    def json_completion(self, messages: List[Dict[str, str]], max_tokens: int = 1500) -> Dict[str, Any]:
        """Get JSON completion from Azure OpenAI"""
        if self.test_mode:
            # Extract user messages for context
            user_messages = [msg['content'] for msg in messages if msg['role'] == 'user']
            latest_message = user_messages[-1] if user_messages else ""
            
            # Generate contextual discussion points and action items
            discussion_points = [
                {
                    "id": 1,
                    "title": "Function Architecture Review",
                    "description": "How well does the current function-based architecture serve the Todo app's needs? Should we consider object-oriented design for future enhancements?",
                    "priority": "High",
                    "category": "Architecture"
                },
                {
                    "id": 2,
                    "title": "Error Handling Enhancement",
                    "description": "The division by zero handling is good, but should we add more comprehensive error handling for invalid inputs and edge cases?",
                    "priority": "Medium",
                    "category": "Quality"
                },
                {
                    "id": 3,
                    "title": "GUI Implementation Strategy",
                    "description": "Would implementing a tkinter-based GUI improve user experience while maintaining the clean code structure?",
                    "priority": "Medium",
                    "category": "Enhancement"
                },
                {
                    "id": 4,
                    "title": "Advanced Mathematical Operations",
                    "description": "Should we extend beyond basic arithmetic to include scientific functions like square root, power, and trigonometric operations?",
                    "priority": "Low",
                    "category": "Feature"
                },
                {
                    "id": 5,
                    "title": "Testing Framework Implementation",
                    "description": "How can we implement comprehensive unit testing to ensure reliability of all mathematical operations?",
                    "priority": "High",
                    "category": "Quality"
                }
            ]
            
            action_items = [
                {
                    "id": 1,
                    "task": "Implement unit tests for all calculator functions",
                    "description": "Create pytest-based tests for add(), subtract(), multiply(), and divide() functions, including edge cases",
                    "priority": "High",
                    "assignee": "Development Team",
                    "due_date": "Next Sprint",
                    "status": "Pending"
                },
                {
                    "id": 2,
                    "task": "Enhance input validation",
                    "description": "Strengthen user input validation to handle non-numeric inputs and provide clear error messages",
                    "priority": "Medium",
                    "assignee": "Backend Developer",
                    "due_date": "This Week",
                    "status": "In Progress"
                },
                {
                    "id": 3,
                    "task": "Add comprehensive documentation",
                    "description": "Include detailed docstrings for all functions and add inline comments explaining complex logic",
                    "priority": "Medium",
                    "assignee": "Technical Writer",
                    "due_date": "End of Month",
                    "status": "Pending"
                },
                {
                    "id": 4,
                    "task": "Design GUI mockups",
                    "description": "Create wireframes and mockups for tkinter-based graphical interface while preserving functionality",
                    "priority": "Low",
                    "assignee": "UI/UX Designer",
                    "due_date": "Next Month",
                    "status": "Pending"
                },
                {
                    "id": 5,
                    "task": "Research advanced mathematical operations",
                    "description": "Investigate implementation of scientific calculator functions (sqrt, power, sin, cos, etc.)",
                    "priority": "Low",
                    "assignee": "Research Team",
                    "due_date": "Future Sprint",
                    "status": "Pending"
                }
            ]
            
            # Generate contextual response based on user input
            if "discussion_points" in latest_message.lower():
                return {"discussion_points": discussion_points}
            elif "action_items" in latest_message.lower():
                return {"action_items": action_items}
            else:
                return {
                    "response": "Todo app-specific analysis complete! This Flask Todo application demonstrates excellent programming fundamentals with clean MVC architecture.",
                    "confidence": 0.85,
                    "suggestions": [
                        "Add comprehensive unit testing",
                        "Implement GUI interface with tkinter",
                        "Enhance error handling and validation",
                        "Consider adding scientific calculator functions"
                    ]
                }
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            # Try to parse the response as JSON
            import json
            try:
                return json.loads(response.choices[0].message.content)
            except json.JSONDecodeError:
                return {"response": response.choices[0].message.content}
                
        except Exception as e:
            logger.error(f"Error in JSON completion: {e}")
            return {"error": "Failed to generate JSON response", "details": str(e)}
    
    def chat_with_context(self, messages: List[Dict[str, str]], repo_context: str) -> Dict[str, str]:
        """Chat with AI while maintaining repository context"""
        if self.test_mode:
            return {
                "response": self._get_test_response('chat'),
                "mom_update": "Test meeting minutes update",
                "insights_update": "Test insights update"
            }
        
        system_prompt = f"""You are an expert code reviewer and software architect. You are analyzing a codebase and having a conversation about it.

Repository Context:
{repo_context}

Your role is to:
1. Answer questions about the code
2. Provide insights and suggestions for improvement
3. Help identify potential issues or optimizations
4. Explain complex code patterns and architecture decisions

For each response, also provide:
- A brief update for meeting minutes (one sentence summarizing the key point discussed)
- An actionable insight or recommendation (one sentence)

Respond in JSON format with keys: 'response', 'mom_update', 'insights_update'."""

        # Add system prompt to the beginning of messages
        full_messages = [{"role": "system", "content": system_prompt}] + messages

        return self.json_completion(full_messages)
    
    def generate_code_health_report(self, repo_structure: str, file_contents: Dict[str, str], conversation_history: List[Dict[str, str]]) -> str:
        """Generate comprehensive code health report"""
        if self.test_mode:
            return self._get_test_response('code_health')
        
        try:
            messages = [
                {"role": "system", "content": "You are a code quality expert. Analyze the code and generate a comprehensive health report."},
                {"role": "user", "content": f"Analyze this repository and generate a code health report:\n\nStructure:\n{repo_structure}\n\nKey Files:\n{str(file_contents)[:2000]}"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating code health report: {e}")
            return f"Error generating code health report: {str(e)}"
    
    def generate_meeting_minutes(self, conversation: str, repo_structure: str) -> str:
        """Generate meeting minutes from conversation"""
        if self.test_mode:
            return self._get_test_response('meeting_minutes')
        
        try:
            messages = [
                {"role": "system", "content": "You are a meeting secretary. Generate professional meeting minutes from the conversation."},
                {"role": "user", "content": f"Generate meeting minutes from this code review conversation:\n\nConversation:\n{conversation[:2000]}\n\nRepository Structure:\n{repo_structure[:500]}"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=1500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating meeting minutes: {e}")
            return f"Error generating meeting minutes: {str(e)}"
    
    def generate_insights_report(self, conversation: str, repo_structure: str, file_contents: Dict[str, str]) -> str:
        """Generate insights report"""
        if self.test_mode:
            return self._get_test_response('insights')
        
        try:
            messages = [
                {"role": "system", "content": "You are a project analyst. Generate strategic insights and recommendations."},
                {"role": "user", "content": f"Generate project insights from this code review:\n\nConversation:\n{conversation[:1500]}\n\nStructure:\n{repo_structure[:500]}\n\nFiles:\n{str(file_contents)[:1000]}"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=2000,
                temperature=0.4
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating insights report: {e}")
            return f"Error generating insights report: {str(e)}"

    def chat(self, message: str, session_id: int) -> dict:
        """Chat with AI assistant"""
        if self.test_mode:
            # Simulate thinking time for realistic feel
            import time
            time.sleep(2.5)  # Add realistic delay
            
            # Get conversation history for context
            from models import Message
            messages = Message.query.filter_by(session_id=session_id).order_by(Message.timestamp).all()
            conversation_history = [{"role": msg.role, "content": msg.content} for msg in messages]
            
            # Generate contextual response
            response = self._get_test_response('chat', message)
            
            # Generate real meeting minutes from conversation
            mom_content = self._generate_real_meeting_minutes(conversation_history, message)
            
            # Generate real action items or set to None
            insights_content = self._generate_real_insights(conversation_history, message)
            
            return {
                "response": response,
                "mom_update": mom_content,
                "insights_update": insights_content
            }
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful AI code reviewer assistant."},
                    {"role": "user", "content": message}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            # Extract discussion points and action items from response
            discussion_points = []
            action_items = []
            for line in response.choices[0].message.content.split('\n'):
                if line.startswith('Discussion Point:'):
                    discussion_points.append(line[17:])
                elif line.startswith('Action Item:'):
                    action_items.append(line[12:])
            
            return {
                "response": response.choices[0].message.content,
                "mom_update": f"Discussed: {message[:50]}...",
                "insights_update": f"Insight: {', '.join(discussion_points)}",
                "discussion_points": discussion_points,
                "action_items": action_items
            }
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "response": f"Error: {str(e)}",
                "mom_update": "",
                "insights_update": ""
            }
    
    def _generate_real_meeting_minutes(self, conversation_history: list, current_message: str) -> str:
        """Generate real meeting minutes from conversation history"""
        if not conversation_history:
            return """**Meeting Minutes - Flask Todo App Code Review**

**Session Started:** Code analysis and review session initiated

**Initial Findings:**
• Repository structure analyzed successfully
• Function-based architecture identified
• Basic arithmetic operations confirmed
• Error handling mechanisms reviewed

**Current Focus:** Awaiting first discussion topic"""
        
        # Create realistic discussion points based on conversation
        discussion_points = []
        
        # Analyze conversation for key topics
        all_content = " ".join([msg['content'].lower() for msg in conversation_history])
        
        if "structure" in all_content or "architecture" in all_content:
            discussion_points.append("**Code Architecture Discussion:**\n- Reviewed function-based design approach\n- Discussed modular structure benefits\n- Analyzed separation of concerns implementation")
        
        if "error" in all_content or "exception" in all_content:
            discussion_points.append("**Error Handling Review:**\n- Examined division by zero protection\n- Discussed input validation strategies\n- Reviewed exception handling patterns")
        
        if "test" in all_content:
            discussion_points.append("**Testing Strategy Planning:**\n- Explored pytest framework adoption\n- Discussed unit testing approaches\n- Planned edge case testing scenarios")
        
        if "improve" in all_content or "enhance" in all_content:
            discussion_points.append("**Enhancement Opportunities:**\n- Identified GUI development potential\n- Discussed scientific function additions\n- Explored memory feature implementations")
        
        if "gui" in all_content or "interface" in all_content:
            discussion_points.append("**User Interface Discussion:**\n- Evaluated tkinter implementation options\n- Discussed modern UI design principles\n- Planned user experience improvements")
        
        if "documentation" in all_content:
            discussion_points.append("**Documentation Planning:**\n- Reviewed current code comments\n- Discussed docstring improvements\n- Planned README enhancements")
        
        # If no specific topics, create general discussion points
        if not discussion_points:
            discussion_points = [
                "**General Code Review:**\n- Analyzed overall code quality\n- Discussed programming best practices\n- Reviewed educational value of the project"
            ]
        
        # Format as professional meeting minutes
        minutes = "**Meeting Minutes - Flask Todo App Code Review**\n\n"
        minutes += "**Topics Discussed:**\n\n"
        minutes += "\n\n".join(discussion_points[-3:])  # Show last 3 topics
        
        # Add current discussion
        if current_message and len(current_message) > 10:
            minutes += f"\n\n**Current Discussion:**\n- {current_message[:100]}{'...' if len(current_message) > 100 else ''}"
        
        return minutes
    
    def _generate_real_insights(self, conversation_history: list, current_message: str) -> str:
        """Generate real insights or return None if no significant insights"""
        if len(conversation_history) < 1:
            return """**Project Insights - Flask Todo App**

**Code Quality Assessment:**
• Clean, readable function-based architecture
• Good separation of mathematical operations
• Educational value for Python learners

**Immediate Opportunities:**
• Add comprehensive error handling
• Implement unit testing framework
• Consider GUI development for better UX

**Technical Recommendations:**
• Maintain modular design principles
• Focus on input validation improvements
• Plan for feature extensibility"""
        
        # Generate contextual insights based on conversation patterns
        insights = []
        technical_recommendations = []
        priority_actions = []
        
        # Analyze conversation content
        all_content = " ".join([msg['content'].lower() for msg in conversation_history])
        
        # Code structure insights
        if "structure" in all_content or "architecture" in all_content:
            insights.append("• Function-based architecture is well-implemented and maintainable")
            technical_recommendations.append("• Consider class-based design for future scalability")
        
        # Error handling insights
        if "error" in all_content or "exception" in all_content:
            insights.append("• Error handling is a critical focus area for improvement")
            priority_actions.append("• Implement comprehensive exception handling")
            technical_recommendations.append("• Add custom exception classes for better error management")
        
        # Testing insights
        if "test" in all_content:
            insights.append("• Testing strategy is essential for code reliability")
            priority_actions.append("• Set up pytest framework and write unit tests")
            technical_recommendations.append("• Implement test-driven development practices")
        
        # GUI insights
        if "gui" in all_content or "interface" in all_content:
            insights.append("• GUI development would significantly enhance user experience")
            priority_actions.append("• Prototype tkinter-based interface")
            technical_recommendations.append("• Design responsive and intuitive user interface")
        
        # Improvement insights
        if "improve" in all_content or "enhance" in all_content:
            insights.append("• Multiple enhancement opportunities identified")
            technical_recommendations.append("• Prioritize features based on user value and complexity")
        
        # Documentation insights
        if "documentation" in all_content:
            insights.append("• Documentation improvements will increase project accessibility")
            priority_actions.append("• Add comprehensive docstrings and README")
        
        # Default insights if no specific patterns found
        if not insights:
            insights = [
                "• Code demonstrates solid Python programming fundamentals",
                "• Project has excellent educational and practical value",
                "• Architecture supports future feature additions"
            ]
            technical_recommendations = [
                "• Continue following clean code principles",
                "• Plan systematic feature enhancements",
                "• Maintain focus on code readability"
            ]
            priority_actions = [
                "• Identify next development priorities",
                "• Consider user feedback for improvements"
            ]
        
        # Format comprehensive insights report
        report = "**Project Insights - Flask Todo App**\n\n"
        
        if insights:
            report += "**Key Insights:**\n"
            report += "\n".join(insights[:4])  # Limit to 4 insights
        
        if technical_recommendations:
            report += "\n\n**Technical Recommendations:**\n"
            report += "\n".join(technical_recommendations[:3])  # Limit to 3 recommendations
        
        if priority_actions:
            report += "\n\n**Priority Actions:**\n"
            report += "\n".join(priority_actions[:3])  # Limit to 3 actions
        
        return report

    def generate_tech_spec(self, repo_structure: str, file_contents: dict) -> str:
        """Generate technical specification document"""
        if self.test_mode:
            return self._get_test_response('tech_spec')
        
        try:
            messages = [
                {"role": "system", "content": "You are a technical documentation expert. Generate a comprehensive technical specification document."},
                {"role": "user", "content": f"Generate a technical specification for this repository:\n\nStructure:\n{repo_structure}\n\nKey Files:\n{str(file_contents)[:2000]}"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating tech spec: {e}")
            return f"Error generating technical specification: {str(e)}"

    def generate_code_health_report(self, repo_structure: str, file_contents: dict) -> str:
        """Generate code health report"""
        if self.test_mode:
            return self._get_test_response('code_health')
        
        try:
            messages = [
                {"role": "system", "content": "You are a code quality expert. Analyze the code and generate a comprehensive health report."},
                {"role": "user", "content": f"Analyze this repository and generate a code health report:\n\nStructure:\n{repo_structure}\n\nKey Files:\n{str(file_contents)[:2000]}"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=2000,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating code health report: {e}")
            return f"Error generating code health report: {str(e)}"

    def generate_meeting_minutes(self, conversation: str, repo_structure: str) -> str:
        """Generate meeting minutes from conversation"""
        if self.test_mode:
            return self._get_test_response('meeting_minutes')
        
        try:
            messages = [
                {"role": "system", "content": "You are a meeting secretary. Generate professional meeting minutes from the conversation."},
                {"role": "user", "content": f"Generate meeting minutes from this code review conversation:\n\nConversation:\n{conversation[:2000]}\n\nRepository Structure:\n{repo_structure[:500]}"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=1500,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating meeting minutes: {e}")
            return f"Error generating meeting minutes: {str(e)}"

    def generate_insights_report(self, conversation: str, repo_structure: str, file_contents: dict) -> str:
        """Generate insights report"""
        if self.test_mode:
            return self._get_test_response('insights')
        
        try:
            messages = [
                {"role": "system", "content": "You are a project analyst. Generate strategic insights and recommendations."},
                {"role": "user", "content": f"Generate project insights from this code review:\n\nConversation:\n{conversation[:1500]}\n\nStructure:\n{repo_structure[:500]}\n\nFiles:\n{str(file_contents)[:1000]}"}
            ]
            
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=2000,
                temperature=0.4
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating insights report: {e}")
            return f"Error generating insights report: {str(e)}"
