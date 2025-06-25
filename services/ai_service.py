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
            
            if not api_key or api_key == 'your_api_key_here':
                logger.warning("Azure OpenAI API key not configured. Running in test mode.")
                self.test_mode = True
                return
                
            if not endpoint or endpoint == 'https://your-resource.openai.azure.com/':
                logger.warning("Azure OpenAI endpoint not configured. Running in test mode.")
                self.test_mode = True
                return
                
            if not deployment or deployment == 'gpt-4':
                logger.warning("Azure OpenAI deployment not configured. Running in test mode.")
                self.test_mode = True
                return
            
            self.client = AzureOpenAI(
                api_key=api_key,
                api_version=os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
                azure_endpoint=endpoint
            )
            self.deployment_name = deployment
            logger.info("Azure OpenAI service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI service: {e}")
            logger.warning("Running in test mode due to initialization error")
            self.test_mode = True
    
    def _get_test_response(self, prompt_type: str) -> str:
        """Generate test responses when Azure OpenAI is not available"""
        test_responses = {
            'chat': "I'm currently running in test mode. To enable full AI functionality, please configure your Azure OpenAI credentials in the .env file.",
            'tech_spec': """# Technical Specification (Test Mode)

## Project Overview
This is a test response generated because Azure OpenAI is not configured.

## Architecture
- **Frontend**: Modern web application
- **Backend**: Flask-based API
- **Database**: SQLite for development

## Key Components
1. Repository analysis system
2. AI-powered chat interface
3. Report generation

## Setup Instructions
To enable full AI functionality:
1. Configure Azure OpenAI credentials in .env file
2. Set AZURE_OPENAI_API_KEY
3. Set AZURE_OPENAI_ENDPOINT
4. Set AZURE_OPENAI_DEPLOYMENT_NAME

*Note: This is a test response. Configure Azure OpenAI for real analysis.*""",
            'code_health': """# Code Health Report (Test Mode)

## Summary
This is a test code health report generated in test mode.

## Findings
- Project structure appears organized
- Azure OpenAI not configured for detailed analysis
- Configure AI service for comprehensive code review

## Recommendations
1. Set up Azure OpenAI credentials
2. Run full analysis with AI enabled
3. Review generated insights and recommendations

*Note: This is a test response. Configure Azure OpenAI for real analysis.*""",
            'meeting_minutes': """# Meeting Minutes (Test Mode)

## Discussion Summary
- Repository analysis initiated
- Test mode active due to missing Azure OpenAI configuration
- System functioning properly in test mode

## Action Items
- [ ] Configure Azure OpenAI credentials
- [ ] Test full AI functionality
- [ ] Review generated reports

*Note: This is a test response. Configure Azure OpenAI for real analysis.*""",
            'insights': """# Insights Report (Test Mode)

## Key Insights
- System is running in test mode
- All core functionality is working
- AI features require Azure OpenAI configuration

## Recommendations
1. Configure Azure OpenAI service
2. Test with real repository analysis
3. Explore full AI capabilities

*Note: This is a test response. Configure Azure OpenAI for real analysis.*"""
        }
        return test_responses.get(prompt_type, "Test response - Azure OpenAI not configured")
    
    def chat_completion(self, messages: List[Dict[str, str]], max_tokens: int = 1000) -> str:
        """Get chat completion from Azure OpenAI"""
        if self.test_mode:
            return self._get_test_response('chat')
            
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
            return {
                "response": self._get_test_response('chat'),
                "mom_update": "Test meeting minutes update",
                "insights_update": "Test insights update"
            }
            
        try:
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error in JSON completion: {e}")
            return {
                "response": f"Error: {str(e)}",
                "mom_update": "",
                "insights_update": ""
            }
    
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
