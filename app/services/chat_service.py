"""
Chat service module for AetherCode application
"""
import random
from app.services.code_reviewer import MOCK_AI_RESPONSES

def process_chat_message(message):
    """Process chat messages and return AI responses"""
    try:
        # In a real implementation, this would call the OpenAI API
        # For now, we'll use mock responses
        
        if any(greeting in message.lower() for greeting in ['hello', 'hi', 'hey']):
            response = random.choice(MOCK_AI_RESPONSES['greetings'])
        else:
            response = f"I received your message: '{message}'. How can I help you with this code?"
        
        return {'message': response}
    except Exception as e:
        return {'error': str(e)}
