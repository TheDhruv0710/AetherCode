/**
 * AetherCode - Chat Functionality
 * Handles chat interactions with the AI assistant
 */

// Initialize chat functionality
document.addEventListener('DOMContentLoaded', () => {
    console.log('Chat.js: Initializing chat functionality');
    initChat();
});

// Chat state
let chatHistory = [];
let isAiTyping = false;

// Initialize chat functionality
function initChat() {
    const chatInput = document.getElementById('chat-input');
    const sendButton = document.querySelector('.send-btn');
    const chatMessages = document.querySelector('.chat-messages');
    
    // Add welcome message
    addAiMessage('Hello! I\'m your AI coding assistant. How can I help you today?');
    
    // Event listeners
    if (sendButton && chatInput) {
        sendButton.addEventListener('click', () => sendMessage());
        
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // Auto-resize the chat input as user types
        chatInput.addEventListener('input', () => {
            chatInput.style.height = 'auto';
            chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
        });
    } else {
        console.error('Chat elements not found');
    }
    
    // Function to send user message
    function sendMessage() {
        if (isAiTyping) return;
        
        const message = chatInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addUserMessage(message);
        
        // Clear input
        chatInput.value = '';
        
        // Get AI response
        getAiResponse(message);
    }
    
    // Add user message to chat
    function addUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.innerHTML = `<p>${escapeHtml(message)}</p>`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Add to chat history
        chatHistory.push({ role: 'user', content: message });
    }
    
    // Add AI message to chat with typing animation
    function addAiMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message ai-message';
        const messageContent = document.createElement('p');
        messageElement.appendChild(messageContent);
        chatMessages.appendChild(messageElement);
        
        // Simulate typing
        isAiTyping = true;
        let i = 0;
        const typingSpeed = 15; // ms per character
        
        function typeNextChar() {
            if (i < message.length) {
                messageContent.innerHTML += escapeHtml(message.charAt(i));
                i++;
                chatMessages.scrollTop = chatMessages.scrollHeight;
                setTimeout(typeNextChar, typingSpeed);
            } else {
                isAiTyping = false;
            }
        }
        
        setTimeout(typeNextChar, 500); // Small delay before starting to type
        
        // Add to chat history
        chatHistory.push({ role: 'assistant', content: message });
    }
    
    // Get AI response
    async function getAiResponse(message) {
        try {
            // Show typing indicator
            const loadingElement = document.createElement('div');
            loadingElement.className = 'message ai-message typing';
            loadingElement.innerHTML = '<div class="typing-indicator"><span></span><span></span><span></span></div>';
            chatMessages.appendChild(loadingElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Get current code from editor
            const code = window.editor ? window.editor.getValue() : '';
            const language = document.getElementById('language-select').value;
            
            // Make API call to backend
            const response = await fetch(`${window.API_BASE_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    code: code,
                    language: language,
                    history: chatHistory
                })
            });
            
            // Remove typing indicator
            chatMessages.removeChild(loadingElement);
            
            if (response.ok) {
                const data = await response.json();
                addAiMessage(data.response || 'I\'m having trouble processing your request.');
            } else {
                // If backend is not available, provide a fallback response
                addAiMessage('I\'m currently unable to connect to the backend. Please make sure the server is running.');
            }
        } catch (error) {
            console.error('Error getting AI response:', error);
            
            // Try to remove typing indicator if it exists
            const typingIndicator = document.querySelector('.typing');
            if (typingIndicator) {
                chatMessages.removeChild(typingIndicator);
            }
            
            addAiMessage('Sorry, I encountered an error. Please make sure the backend server is running.');
        }
    }
    
    // Helper function to escape HTML
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
}

// Export functions for use in other modules
window.chatModule = {
    addAiMessage: function(message) {
        const chatMessages = document.querySelector('.chat-messages');
        if (!chatMessages) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = 'message ai-message';
        messageElement.innerHTML = `<p>${message}</p>`;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Add to chat history
        chatHistory.push({ role: 'assistant', content: message });
    }
};
