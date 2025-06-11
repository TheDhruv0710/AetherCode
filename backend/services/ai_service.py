"""
AI Service for AetherCode

This service handles interactions with AI models for code analysis and chat functionality.
"""

import os
import logging
import json
from typing import List, Dict, Any, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class AIService:
    """
    Service for AI-powered code analysis and chat functionality.
    """
    
    def __init__(self):
        """Initialize the AI service with API keys and configurations"""
        # Get API key from environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("AI_MODEL", "gpt-4")
        
        # Check if API key is available
        if not self.api_key:
            logger.warning("No OpenAI API key found. Set OPENAI_API_KEY environment variable for AI functionality.")
        
        # Initialize conversation context
        self.system_prompt = """
        You are AetherCode AI, an intelligent code assistant. Your purpose is to help users with:
        1. Code review and analysis
        2. Bug identification and fixes
        3. Best practices and optimization suggestions
        4. Answering programming questions
        5. Explaining code concepts
        
        Be concise, helpful, and focus on providing practical advice. When analyzing code, consider:
        - Code quality and readability
        - Potential bugs or edge cases
        - Performance optimizations
        - Security considerations
        - Best practices for the specific language
        
        If you're unsure about something, acknowledge it rather than making assumptions.
        """
    
    def get_response(self, 
                    user_message: str, 
                    conversation_history: List[Dict[str, str]] = None,
                    code_context: str = None,
                    language: str = "javascript") -> str:
        """
        Get AI response for a user message
        
        Args:
            user_message: The user's message
            conversation_history: Previous messages in the conversation
            code_context: Current code in the editor (optional)
            language: Programming language of the code (optional)
            
        Returns:
            AI response as a string
        """
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            logger.warning("No valid OpenAI API key found. Using mock response.")
            return self._get_mock_response(user_message, code_context, language)
        
        try:
            # Prepare conversation history
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history if available
            if conversation_history:
                for msg in conversation_history:
                    messages.append(msg)
            
            # Add code context if available
            if code_context:
                code_message = f"I'm working with this {language} code:\n```{language}\n{code_context}\n```"
                messages.append({"role": "user", "content": code_message})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI API
            response = self._call_openai_api(messages)
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def analyze_code(self, 
                    code: str, 
                    language: str = "javascript", 
                    analysis_type: str = "general") -> Dict[str, Any]:
        """
        Analyze code using AI
        
        Args:
            code: Source code to analyze
            language: Programming language
            analysis_type: Type of analysis (general, security, performance, etc.)
            
        Returns:
            Dictionary with analysis results
        """
        if not self.api_key or self.api_key == "your_openai_api_key_here":
            logger.warning("No valid OpenAI API key found. Using mock analysis response.")
            mock_response = self._get_mock_response(f"Please analyze this {language} code", code, language)
            return {
                "summary": "Demo analysis (no API key)",
                "details": mock_response,
                "mock": True
            }
        
        try:
            # Create a prompt based on analysis type
            prompt = self._create_analysis_prompt(analysis_type, language)
            
            # Prepare messages
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"```{language}\n{code}\n```"}
            ]
            
            # Call OpenAI API
            response = self._call_openai_api(messages)
            
            # Parse the response
            analysis_result = self._parse_analysis_response(response)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing code with AI: {str(e)}")
            return {"error": str(e)}
    
    def _call_openai_api(self, messages: List[Dict[str, str]]) -> str:
        """
        Call OpenAI API with messages
        
        Args:
            messages: List of message dictionaries
            
        Returns:
            AI response as a string
        """
        try:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 2000
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return f"API error: {response.status_code}"
                
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {str(e)}")
            raise
    
    def _create_analysis_prompt(self, analysis_type: str, language: str) -> str:
        """
        Create a prompt for code analysis based on analysis type
        
        Args:
            analysis_type: Type of analysis
            language: Programming language
            
        Returns:
            Prompt string
        """
        base_prompt = "You are an expert code reviewer specializing in " + language + "."
        
        if analysis_type == "security":
            return base_prompt + """
            Analyze the following code for security vulnerabilities and risks.
            Focus on:
            1. Injection vulnerabilities
            2. Authentication issues
            3. Data exposure
            4. Security misconfigurations
            5. Using components with known vulnerabilities
            6. Insecure cryptographic storage
            
            Format your response as JSON with these sections:
            - vulnerabilities: List of identified security issues
            - risk_level: Overall risk assessment (low, medium, high)
            - recommendations: Specific fixes for each vulnerability
            """
            
        elif analysis_type == "performance":
            return base_prompt + """
            Analyze the following code for performance optimizations.
            Focus on:
            1. Algorithmic efficiency
            2. Resource usage
            3. Memory management
            4. Bottlenecks
            5. Unnecessary operations
            
            Format your response as JSON with these sections:
            - issues: List of performance issues
            - impact: Impact assessment for each issue (low, medium, high)
            - optimizations: Specific optimization suggestions
            """
            
        else:  # general analysis
            return base_prompt + """
            Analyze the following code for quality, readability, and best practices.
            Focus on:
            1. Code structure and organization
            2. Naming conventions
            3. Error handling
            4. Documentation
            5. Adherence to language best practices
            6. Potential bugs or edge cases
            
            Format your response as JSON with these sections:
            - issues: List of identified issues
            - suggestions: Improvement recommendations
            - positive_aspects: Good practices already present in the code
            """
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """
        Parse AI response into structured analysis
        
        Args:
            response: AI response string
            
        Returns:
            Structured analysis dictionary
        """
        try:
            # Try to extract JSON from the response
            json_start = response.find('{')
            json_end = response.rfind('}')
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end+1]
                return json.loads(json_str)
            
            # If no JSON found, return the response as a general analysis
            return {
                "general_analysis": response,
                "format": "text"
            }
            
        except json.JSONDecodeError:
            # If JSON parsing fails, return the response as text
            return {
                "general_analysis": response,
                "format": "text"
            }
            
    def _get_mock_response(self, user_message: str, code_context: str = None, language: str = "javascript") -> str:
        """
        Generate a mock response when no valid API key is available
        
        Args:
            user_message: The user's message
            code_context: Current code in the editor (optional)
            language: Programming language of the code (optional)
            
        Returns:
            Mock AI response as a string
        """
        # Simple mock responses based on message content
        if "hello" in user_message.lower() or "hi" in user_message.lower():
            return "Hello! I'm AetherCode AI. I can help you with code review, bug fixes, and programming questions. Note that I'm currently running in demo mode without an OpenAI API key."
        
        if "help" in user_message.lower():
            return "I can help you with code review, bug identification, optimization suggestions, and answering programming questions. Currently running in demo mode without an OpenAI API key."
            
        if "review" in user_message.lower() or "analyze" in user_message.lower():
            if code_context:
                return f"I've analyzed your {language} code. This is a demo response as no valid OpenAI API key is configured. In a real implementation, I would provide detailed code review with suggestions for improvements."
            else:
                return "Please provide some code for me to review. Note that I'm currently running in demo mode without an OpenAI API key."
                
        if "error" in user_message.lower() or "bug" in user_message.lower():
            return "I can help identify bugs in your code. In this demo mode (no API key), I can't provide detailed analysis. Please configure a valid OpenAI API key in the .env file for full functionality."
            
        # Default response
        return "I'm running in demo mode without an OpenAI API key. To enable full AI functionality, please add a valid OpenAI API key to the .env file in the backend directory. For now, I can only provide basic responses."
