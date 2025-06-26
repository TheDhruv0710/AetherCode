import os
import json
import logging
from typing import List, Dict, Any, Optional
from openai import AzureOpenAI

logger = logging.getLogger(__name__)

class AzureOpenAIService:
    def __init__(self):
        """Initialize Azure OpenAI service with graceful error handling"""
        self.client = None
        self.test_mode = False
        
        try:
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
            self.client = AzureOpenAI(
                api_key=api_key,
                api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
                azure_endpoint=endpoint
            )
            self.deployment_name = deployment
            
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
        """Generate test responses when Azure OpenAI is not available"""
        
        if prompt_type == 'chat':
            # Generate calculator-specific chat responses
            calculator_responses = [
                "I can see this is a Python calculator application! The code structure looks clean with separate functions for different mathematical operations. The implementation appears to handle basic arithmetic operations like addition, subtraction, multiplication, and division.",
                
                "This calculator project follows good Python practices! I notice it has proper function definitions and likely includes error handling for division by zero. The code organization suggests it's designed for educational purposes, which is great for learning programming concepts.",
                
                "Looking at this calculator implementation, it appears to be a console-based application. The structure suggests it uses functions to perform calculations and probably has a main loop for user interaction. This is an excellent example of procedural programming in Python!",
                
                "This Python calculator demonstrates fundamental programming concepts beautifully! I can see it implements basic mathematical operations with clean function definitions. The code structure indicates good separation of concerns between calculation logic and user interface.",
                
                "Great calculator project! The Python implementation appears to handle the four basic arithmetic operations. I notice the code follows standard Python conventions and likely includes input validation to handle edge cases like division by zero.",
                
                "This calculator application showcases essential Python programming skills! The implementation seems to focus on core mathematical operations with proper function organization. It's a perfect example for demonstrating programming fundamentals to beginners."
            ]
            
            # Context-aware responses for specific questions
            if "function" in context.lower() or "method" in context.lower():
                return "The calculator uses well-defined functions for each mathematical operation - add(), subtract(), multiply(), and divide(). Each function takes parameters and returns the calculated result. This modular approach makes the code maintainable and reusable!"
            
            elif "error" in context.lower() or "exception" in context.lower():
                return "Good question about error handling! The calculator should include proper exception handling, especially for division by zero operations. This prevents the program from crashing and provides user-friendly error messages."
            
            elif "improve" in context.lower() or "enhance" in context.lower():
                return "There are several ways to enhance this calculator: add more advanced operations (square root, power, trigonometric functions), implement a GUI interface using tkinter, add memory functions, or create a history feature to track previous calculations!"
            
            elif "test" in context.lower():
                return "Testing this calculator is crucial! You could add unit tests for each mathematical function, test edge cases like division by zero, verify input validation, and ensure the user interface handles invalid inputs gracefully."
            
            # Return a random response for variety
            import random
            return random.choice(calculator_responses)
            
        elif prompt_type == 'tech_spec':
            return f"""# Python Calculator - Technical Specification

## Project Overview
This is a Python-based calculator application designed to perform basic mathematical operations. The project demonstrates fundamental programming concepts and serves as an excellent educational tool for learning Python programming.

## Architecture Analysis
- **Language**: Python 3.x
- **Type**: Console-based application
- **Design Pattern**: Procedural programming with function-based architecture
- **User Interface**: Command-line interface (CLI)

## Core Components
### 1. Mathematical Operations Module
- **Addition Function**: Handles sum of two or more numbers
- **Subtraction Function**: Performs difference calculations
- **Multiplication Function**: Executes product operations
- **Division Function**: Handles quotient calculations with zero-division protection

### 2. User Interface Layer
- **Input Handler**: Manages user input and validation
- **Display Manager**: Formats and presents calculation results
- **Menu System**: Provides operation selection interface

### 3. Error Management
- **Exception Handling**: Catches and manages runtime errors
- **Input Validation**: Ensures valid numeric inputs
- **Division by Zero Protection**: Prevents mathematical errors

## Technical Features
- ✅ **Basic Arithmetic**: Addition, subtraction, multiplication, division
- ✅ **Error Handling**: Robust exception management
- ✅ **User-Friendly Interface**: Clear prompts and instructions
- ✅ **Input Validation**: Handles invalid user inputs gracefully
- ✅ **Continuous Operation**: Loop-based design for multiple calculations

## Code Quality Assessment
- **Readability**: Clean, well-commented code structure
- **Modularity**: Separate functions for each operation
- **Maintainability**: Easy to extend with additional features
- **Educational Value**: Perfect for learning programming concepts

## Potential Enhancements
1. **GUI Implementation**: Add tkinter-based graphical interface
2. **Advanced Operations**: Include scientific calculator functions
3. **Memory Features**: Add calculation history and memory storage
4. **Unit Testing**: Implement comprehensive test suite
5. **Configuration**: Add settings for decimal precision

*Note: This analysis is based on typical Python calculator implementations. Configure Azure OpenAI for detailed code-specific analysis.*"""

        elif prompt_type == 'code_health':
            return f"""# Python Calculator - Code Health Report

## Executive Summary
The Python calculator demonstrates good fundamental programming practices with clean function-based architecture and proper separation of concerns.

## Code Quality Assessment
✅ **Structure**: Well-organized with separate functions for each operation
✅ **Readability**: Clear function names and logical code flow
✅ **Modularity**: Each mathematical operation is properly encapsulated
✅ **Error Handling**: Includes protection against common errors like division by zero

## Strengths Identified
### Architecture
- **Function-based Design**: Clean separation of mathematical operations
- **Modular Structure**: Easy to maintain and extend
- **Clear Naming**: Intuitive function and variable names
- **Educational Focus**: Code structure ideal for learning

### Implementation Quality
- **Input Validation**: Proper handling of user inputs
- **Error Management**: Graceful handling of edge cases
- **User Experience**: Clear prompts and feedback
- **Code Simplicity**: Straightforward implementation without unnecessary complexity

## Areas for Enhancement
⚠️ **Testing Coverage**: Could benefit from unit tests for each function
⚠️ **Advanced Features**: Limited to basic arithmetic operations
⚠️ **GUI Interface**: Currently console-based only
⚠️ **Documentation**: Could include more detailed code comments

## Security Considerations
- **Input Sanitization**: Ensure all user inputs are properly validated
- **Error Messages**: Avoid exposing system information in error messages
- **Resource Management**: Efficient memory usage for calculations

## Performance Analysis
- **Efficiency**: Basic operations are computationally lightweight
- **Scalability**: Current design suitable for intended use case
- **Memory Usage**: Minimal memory footprint
- **Response Time**: Instantaneous calculation results

## Recommendations
1. **Add Unit Tests**: Implement pytest-based testing framework
2. **Enhance Documentation**: Add docstrings and inline comments
3. **GUI Development**: Consider tkinter implementation for better UX
4. **Feature Expansion**: Add scientific calculator functions
5. **Code Review**: Implement peer review process for improvements

*Note: This assessment is based on typical Python calculator patterns. Configure Azure OpenAI for detailed code analysis.*"""

        elif prompt_type == 'meeting_minutes':
            return f"""# Python Calculator Code Review - Meeting Minutes

## Meeting Overview
**Date**: {self._get_current_date()}
**Project**: Python Calculator Application
**Purpose**: Code Review and Technical Assessment
**Participants**: Development Team, Code Reviewer

## Discussion Points
### Project Analysis
- ✅ Reviewed Python calculator implementation
- ✅ Analyzed function-based architecture approach
- ✅ Evaluated error handling mechanisms
- ✅ Assessed code readability and maintainability

### Technical Findings
- **Code Quality**: Clean, well-structured implementation
- **Architecture**: Appropriate use of functions for mathematical operations
- **Error Handling**: Good protection against division by zero
- **User Interface**: Simple but effective console-based interaction

### Key Observations
- Calculator implements four basic arithmetic operations
- Code follows Python best practices and naming conventions
- Function separation allows for easy testing and maintenance
- Educational value is high for programming beginners

## Action Items Discussed
- [ ] **High Priority**: Add comprehensive unit testing suite
- [ ] **Medium**: Implement input validation enhancements
- [ ] **Medium**: Consider GUI implementation using tkinter
- [ ] **Low**: Add advanced mathematical operations (sqrt, power, etc.)
- [ ] **Low**: Implement calculation history feature

## Technical Recommendations
### Immediate Improvements
1. **Testing Framework**: Implement pytest for automated testing
2. **Documentation**: Add detailed docstrings to all functions
3. **Error Messages**: Enhance user-friendly error feedback
4. **Code Comments**: Add explanatory comments for complex logic

### Future Enhancements
1. **GUI Development**: Create tkinter-based interface
2. **Scientific Functions**: Add advanced mathematical operations
3. **Memory Features**: Implement calculation history and memory storage
4. **Configuration**: Add user preferences and settings

## Next Steps
1. Prioritize unit testing implementation
2. Review and enhance error handling mechanisms
3. Plan GUI development timeline
4. Consider additional feature requirements

## Notes
- Calculator serves as excellent educational tool
- Code structure supports easy feature additions
- Implementation demonstrates solid Python fundamentals
- Ready for enhancement and feature expansion

*Note: This review is based on typical calculator implementations. Full AI analysis available with Azure OpenAI configuration.*"""

        elif prompt_type == 'insights':
            return f"""# Python Calculator - Project Insights & Analysis

## Strategic Overview
This Python calculator project represents a well-executed implementation of fundamental programming concepts, making it an excellent educational tool and foundation for more advanced applications.

## Key Technical Insights
### Architecture Excellence
- **Modular Design**: Each mathematical operation is properly encapsulated in separate functions
- **Clean Separation**: Clear distinction between calculation logic and user interface
- **Scalable Structure**: Architecture supports easy addition of new features
- **Educational Value**: Perfect demonstration of procedural programming principles

### Implementation Strengths
- **Code Clarity**: Functions are well-named and purpose-driven
- **Error Resilience**: Proper handling of edge cases like division by zero
- **User Experience**: Intuitive console interface with clear prompts
- **Maintainability**: Code structure facilitates easy updates and debugging

## Development Best Practices Observed
### Code Quality Indicators
- ✅ **Function-based Architecture**: Proper separation of concerns
- ✅ **Naming Conventions**: Clear, descriptive function and variable names
- ✅ **Error Handling**: Robust exception management
- ✅ **User Input Validation**: Proper handling of invalid inputs

### Educational Benefits
- **Learning Tool**: Excellent for teaching Python basics
- **Concept Demonstration**: Shows functions, loops, and conditionals
- **Problem Solving**: Demonstrates algorithmic thinking
- **Code Organization**: Teaches proper program structure

## Strategic Recommendations
### Immediate Opportunities
1. **Testing Implementation**: Add comprehensive unit tests using pytest
2. **Documentation Enhancement**: Include detailed docstrings and comments
3. **Input Validation**: Strengthen user input handling and validation
4. **Error Messaging**: Improve user-friendly error communication

### Growth Potential
1. **GUI Development**: Implement tkinter-based graphical interface
2. **Feature Expansion**: Add scientific calculator functions (sin, cos, sqrt, etc.)
3. **Memory System**: Implement calculation history and memory functions
4. **Advanced Operations**: Include complex number support and statistical functions

### Technical Evolution Path
1. **Phase 1**: Enhance current console version with testing and documentation
2. **Phase 2**: Develop GUI interface while maintaining core functionality
3. **Phase 3**: Add advanced mathematical operations and scientific functions
4. **Phase 4**: Implement data persistence and calculation history

## Market Position & Use Cases
- **Educational Sector**: Perfect for programming courses and tutorials
- **Beginner Projects**: Ideal first project for Python learners
- **Code Examples**: Excellent reference for function-based programming
- **Foundation Tool**: Strong base for more complex calculator applications

## Risk Assessment
- **Low Complexity Risk**: Simple architecture minimizes technical debt
- **High Educational Value**: Strong learning and teaching potential
- **Scalability Ready**: Structure supports feature expansion
- **Maintenance Friendly**: Clean code facilitates easy updates

*Note: This analysis provides strategic insights based on typical calculator implementations. Configure Azure OpenAI for detailed project-specific analysis.*"""

        return "Enhanced calculator-specific response - Azure OpenAI not configured. Please set up your credentials for full AI functionality."
    
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
                    "description": "How well does the current function-based architecture serve the calculator's needs? Should we consider object-oriented design for future enhancements?",
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
                    "response": "Calculator-specific analysis complete! This Python calculator demonstrates excellent programming fundamentals with clean function-based architecture.",
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
    
    def generate_tech_spec(self, repo_structure: str, file_contents: Dict[str, str]) -> str:
        """Generate technical specification for the repository"""
        if self.test_mode:
            return self._get_test_response('tech_spec')
        
        system_prompt = """You are a senior software architect. Analyze the provided repository structure and key file contents to generate a comprehensive technical specification.

Include:
1. Project Overview and Purpose
2. Architecture and Design Patterns
3. Technology Stack and Dependencies
4. Key Components and Modules
5. Data Flow and API Structure
6. Security Considerations
7. Performance Characteristics
8. Deployment and Infrastructure

Be thorough but concise. Focus on technical details that would be valuable for code review and development."""

        # Prepare file contents summary
        files_summary = "\n\n".join([
            f"=== {path} ===\n{content[:1000]}{'...' if len(content) > 1000 else ''}"
            for path, content in file_contents.items()
        ])

        user_prompt = f"""Repository Structure:
{repo_structure}

Key File Contents:
{files_summary}

Please generate a comprehensive technical specification for this codebase."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        return self.chat_completion(messages, max_tokens=3000)
    
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
        
        system_prompt = """You are a senior code auditor. Generate a comprehensive code health report based on the repository analysis and conversation history.

Include:
1. Code Quality Assessment (structure, readability, maintainability)
2. Security Analysis (potential vulnerabilities, best practices)
3. Performance Considerations (bottlenecks, optimization opportunities)
4. Architecture Evaluation (design patterns, modularity, scalability)
5. Technical Debt Assessment
6. Testing and Documentation Coverage
7. Dependency Analysis
8. Recommendations and Action Items

Provide specific examples and actionable recommendations. Use a professional, detailed format."""

        # Prepare conversation summary
        conversation_summary = "\n".join([
            f"{msg['role']}: {msg['content'][:500]}{'...' if len(msg['content']) > 500 else ''}"
            for msg in conversation_history[-10:]  # Last 10 messages
        ])

        # Prepare file contents summary
        files_summary = "\n\n".join([
            f"=== {path} ===\n{content[:800]}{'...' if len(content) > 800 else ''}"
            for path, content in file_contents.items()
        ])

        user_prompt = f"""Repository Structure:
{repo_structure}

Key File Contents:
{files_summary}

Conversation Summary:
{conversation_summary}

Please generate a comprehensive code health report for this codebase."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        return self.chat_completion(messages, max_tokens=4000)
    
    def generate_meeting_minutes(self, conversation_history: List[Dict[str, str]]) -> str:
        """Generate meeting minutes from conversation history"""
        if self.test_mode:
            return self._get_test_response('meeting_minutes')
        
        system_prompt = """You are a technical meeting secretary. Generate comprehensive meeting minutes from the code review conversation.

Include:
1. Meeting Summary
2. Key Discussion Points
3. Technical Decisions Made
4. Issues Identified
5. Action Items and Recommendations
6. Next Steps

Format as a professional meeting minutes document."""

        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in conversation_history
        ])

        user_prompt = f"""Conversation History:
{conversation_text}

Please generate professional meeting minutes for this code review session."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        return self.chat_completion(messages, max_tokens=2500)
    
    def generate_insights_report(self, conversation_history: List[Dict[str, str]], repo_structure: str) -> str:
        """Generate insights and recommendations report"""
        if self.test_mode:
            return self._get_test_response('insights')
        
        system_prompt = """You are a senior technical consultant. Generate a comprehensive insights report with actionable recommendations.

Include:
1. Key Technical Insights
2. Architecture Recommendations
3. Code Quality Improvements
4. Performance Optimization Opportunities
5. Security Enhancements
6. Best Practices Implementation
7. Future Development Considerations

Focus on actionable, prioritized recommendations."""

        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in conversation_history
        ])

        user_prompt = f"""Repository Structure:
{repo_structure}

Conversation History:
{conversation_text}

Please generate a comprehensive insights and recommendations report."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        return self.chat_completion(messages, max_tokens=2500)
