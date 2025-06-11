/**
 * AetherCode - Main Application Logic
 */

// API Base URL - Change this to match your backend server
window.API_BASE_URL = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    console.log('Main.js: DOM content loaded');
    
    // Initialize submit button
    initSubmitButton();
    
    // Initialize run code button
    const runButton = document.getElementById('run-button');
    if (runButton) {
        console.log('Run button found, adding event listener');
        runButton.addEventListener('click', runCode);
    } else {
        console.error('Run button not found!');
    }
    
    // Initialize clear output button
    const clearOutputButton = document.getElementById('clear-output');
    if (clearOutputButton) {
        console.log('Clear output button found, adding event listener');
        clearOutputButton.addEventListener('click', clearOutput);
    } else {
        console.error('Clear output button not found!');
    }
    
    // Initialize clear chat button
    const clearChatButton = document.getElementById('clear-chat');
    if (clearChatButton) {
        console.log('Clear chat button found, adding event listener');
        clearChatButton.addEventListener('click', clearChat);
    } else {
        console.error('Clear chat button not found!');
    }
    
    // Add drag and drop styling
    initDragAndDropStyling();
    
    // Add initial welcome message with typing animation
    setTimeout(() => {
        addAIMessage("Hello! I'm your AI code reviewer. Submit your code, and I'll provide feedback and suggestions to improve it.");
    }, 600);
});

// Auto-resize function for textareas
function autoResizeTextarea(textarea) {
    if (!textarea) return;
    
    textarea.addEventListener('input', () => {
        textarea.style.height = 'auto';
        textarea.style.height = textarea.scrollHeight + 'px';
    });
}

// Store conversation history
window.conversationHistory = window.conversationHistory || [];

// Send a message from the chat input
function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    
    if (message === '') return;
    
    // Add user message to chat
    addUserMessage(message);
    
    // Store user message in history
    window.conversationHistory.push({
        role: 'user',
        content: message
    });
    
    // Clear input and reset height
    chatInput.value = '';
    chatInput.style.height = '45px';
    
    // Show typing indicator immediately
    showTypingIndicator();
    
    // Get current code from editor for context
    const code = window.getEditorCode ? window.getEditorCode() : '';
    const language = window.getSelectedLanguage ? window.getSelectedLanguage() : 'javascript';
    
    // Send chat message to backend
    sendChatMessage(message, code, language)
        .then(response => {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add AI response with typing animation
            addAIMessage(response);
            
            // Store AI response in history
            window.conversationHistory.push({
                role: 'assistant',
                content: response
            });
        })
        .catch(error => {
            console.error('Chat error:', error);
            removeTypingIndicator();
            addAIMessage("Sorry, I encountered an error. Please try again later.");
        });
}

// Send chat message to backend
async function sendChatMessage(message, codeContext, language) {
    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                conversation_history: window.conversationHistory,
                code_context: codeContext,
                language: language
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Add user message to chat
function addUserMessage(text) {
    const chatMessages = document.querySelector('.chat-messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const messagePara = document.createElement('p');
    messagePara.textContent = text;
    
    messageContent.appendChild(messagePara);
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add AI message to chat with typing animation effect
// Expose to window object so it can be used from editor.js
window.addAIMessage = function(text) {
    const chatMessages = document.querySelector('.chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message ai-message';
    
    // Create avatar
    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
    messageDiv.appendChild(avatar);
    
    // Create message content with typing animation
    const content = document.createElement('div');
    content.className = 'content';
    messageDiv.appendChild(content);
    
    // Append message to chat
    chatMessages.appendChild(messageDiv);
    
    // Animate typing
    animateTyping(content, text);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Animate typing effect character by character
// Expose to window object so it can be used from editor.js
window.animateTyping = function(element, text) {
    let index = 0;
    const typingSpeed = 30; // milliseconds per character
    
    // Clear any existing content
    element.textContent = '';
    
    // Add typing indicator
    const typingIndicator = document.createElement('span');
    typingIndicator.className = 'typing-indicator';
    element.appendChild(typingIndicator);
    
    // Type each character with a delay
    function typeNextChar() {
        if (index < text.length) {
            // Remove typing indicator before adding character
            if (element.contains(typingIndicator)) {
                element.removeChild(typingIndicator);
            }
            
            // Add the next character
            element.textContent += text[index];
            
            // Re-add typing indicator
            element.appendChild(typingIndicator);
            
            index++;
            
            // Random slight variation in typing speed for realism
            const randomDelay = typingSpeed + Math.random() * 20 - 10;
            setTimeout(typeNextChar, randomDelay);
        } else {
            // Remove typing indicator when done
            if (element.contains(typingIndicator)) {
                element.removeChild(typingIndicator);
            }
        }
    }
    
    // Start typing animation
    setTimeout(typeNextChar, 300); // Small initial delay
}

// Run code and display output
async function runCode() {
    console.log('Run code function called');
    
    // Make sure we have access to the editor
    if (typeof window.editor === 'undefined') {
        console.error('Editor is not available!');
        setOutput('// Error: Editor not initialized', 'error');
        setExecutionStatus('Error', 'error');
        setExecutionTime('0 ms');
        return;
    }
    
    // Get code directly from the editor instance
    const code = window.editor.getValue();
    const languageSelect = document.getElementById('language-select');
    const language = languageSelect ? languageSelect.value : 'javascript';
    
    console.log('Executing code:', code);
    console.log('Language:', language);
    
    if (!code || !code.trim()) {
        setOutput('// No code to execute', 'error');
        setExecutionStatus('Error', 'error');
        setExecutionTime('0 ms');
        return;
    }
    
    // Clear previous output
    clearOutput();
    
    // Show loading in output
    setOutput('// Executing code...');
    setExecutionStatus('Running', '');
    
    try {
        console.log(`Sending request to ${API_BASE_URL}/execute`);
        
        // Check if backend is running first
        try {
            const healthCheck = await fetch(`${API_BASE_URL.split('/api')[0]}/health`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!healthCheck.ok) {
                throw new Error('Backend server is not responding');
            }
        } catch (healthError) {
            console.error('Backend health check failed:', healthError);
            setOutput('// Error: Backend server is not running or not accessible.\n// Please start the backend server using:\n// cd backend && python run_backend.py');
            setExecutionStatus('Error', 'error');
            setExecutionTime('0 ms');
            return;
        }
        
        const response = await fetch(`${API_BASE_URL}/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                language: language
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.success) {
            setOutput(data.output || '// No output');
            setExecutionStatus('Success', 'success');
            if (data.execution_time) {
                setExecutionTime(data.execution_time);
            }
        } else {
            setOutput(data.error || '// Execution failed');
            setExecutionStatus('Error', 'error');
        }
        
        setExecutionTime(`${data.execution_time} s`);
        
    } catch (error) {
        console.error('Error executing code:', error);
        setOutput(`// Error: ${error.message}\n// Make sure the backend server is running:\n// cd backend && python run_backend.py`);
        setExecutionStatus('Error', 'error');
        setExecutionTime('0 ms');
    }
}

// Set output content
function setOutput(text, type = '') {
    const outputContent = document.getElementById('output-content');
    outputContent.textContent = text;
    outputContent.className = type;
    
    // Scroll to top of output
    document.getElementById('output-window').scrollTop = 0;
}

// Clear output
function clearOutput() {
    setOutput('// Code execution output will appear here');
    setExecutionStatus('', '');
    setExecutionTime('');
}

// Clear chat messages and history
function clearChat() {
    // Clear chat messages from UI
    const chatMessages = document.querySelector('.chat-messages');
    if (chatMessages) {
        chatMessages.innerHTML = '';
    }
    
    // Clear chat history
    window.conversationHistory = [];
    
    // Add welcome message back
    addAIMessage("Hello! I'm your AI coding assistant. How can I help you today?");
}

// Set execution status
function setExecutionStatus(text, className) {
    const statusElement = document.getElementById('execution-status');
    statusElement.textContent = text;
    statusElement.className = 'execution-status';
    
    if (className) {
        statusElement.classList.add(className);
    }
}

// Set execution time
function setExecutionTime(text) {
    document.getElementById('execution-time').textContent = text;
}

// API base URL
const API_BASE_URL = 'http://localhost:5000/api';

// Reference to the editor from editor.js
let editor; // Will be set from editor.js

// Get editor code
function getEditorCode() {
    return editor ? editor.getValue() : '';
}

// Get selected language
function getSelectedLanguage() {
    const languageSelect = document.getElementById('language-select');
    return languageSelect ? languageSelect.value : 'javascript';
};

// Initialize submit button
function initSubmitButton() {
    const submitBtn = document.getElementById('submit-code-review');
    
    if (!submitBtn) {
        console.error('Submit code review button not found!');
        return;
    }
    
    submitBtn.addEventListener('click', () => {
        // Get code from CodeMirror editor using our global function
        const code = window.getEditorCode ? window.getEditorCode() : '';
        const codeFileInput = document.getElementById('code-file-input');
        const projectFilesInput = document.getElementById('project-files-input');
        
        // Check if we have code to submit
        if (code.trim() === '' && 
            codeFileInput.files.length === 0 && 
            projectFilesInput.files.length === 0) {
            
            addAIMessage("Please enter code in the editor or upload a file before submitting.");
            return;
        }
        
        // Get the selected language
        const language = window.getSelectedLanguage ? window.getSelectedLanguage() : 'javascript';
        const languageDisplay = window.getSelectedLanguageDisplayName ? window.getSelectedLanguageDisplayName() : 'code';
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Processing...</span><i class="fas fa-spinner fa-spin"></i>';
        
        // Show typing indicator immediately
        showTypingIndicator();
        
        // Send code to backend API for analysis
        analyzeCode(code, language)
            .then(result => {
                // Process analysis result
                processAnalysisResult(result, languageDisplay);
            })
            .catch(error => {
                console.error('Error analyzing code:', error);
                removeTypingIndicator();
                addAIMessage(`Sorry, I encountered an error while analyzing your code. Please try again later.`);
            })
            .finally(() => {
                // Reset button
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<span>Submit Code for Review</span><i class="fas fa-arrow-right"></i>';
            });
    });
}

// Send code to backend for analysis
async function analyzeCode(code, language) {
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                language: language
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// Process analysis result and display to user
function processAnalysisResult(result, languageDisplay) {
    // Remove the standalone typing indicator
    removeTypingIndicator();
    
    if (result.error) {
        addAIMessage(`Error analyzing code: ${result.error}`);
        return;
    }
    
    // Format the analysis results into a user-friendly message
    let message = `I've analyzed your ${languageDisplay} code. Here's what I found:\n\n`;
    
    // Add metrics
    const metrics = result.metrics || {};
    message += `**Code Metrics:**\n`;
    message += `- Total lines: ${metrics.total_lines || 'N/A'}\n`;
    message += `- Code lines: ${metrics.code_lines || 'N/A'}\n`;
    message += `- Comment lines: ${metrics.comment_lines || 'N/A'} (${metrics.comment_ratio || 0}%)\n\n`;
    
    // Add issues
    const analysis = result.analysis || {};
    const issues = analysis.issues || [];
    
    if (issues.length > 0) {
        message += `**Issues Found:**\n`;
        issues.forEach((issue, index) => {
            message += `${index + 1}. **${issue.type || 'Issue'}**: ${issue.message || 'No details'}\n`;
        });
        message += '\n';
    } else {
        message += `**No significant issues found.**\n\n`;
    }
    
    // Add suggestions
    const suggestions = analysis.suggestions || [];
    if (suggestions.length > 0) {
        message += `**Suggestions:**\n`;
        suggestions.forEach((suggestion, index) => {
            message += `${index + 1}. ${suggestion}\n`;
        });
        message += '\n';
    }
    
    // Add insights
    const insights = analysis.insights || [];
    if (insights.length > 0) {
        message += `**Insights:**\n`;
        insights.forEach((insight, index) => {
            message += `${index + 1}. ${insight}\n`;
        });
    }
    
    // Show the formatted message with typing animation
    addAIMessage(message);
    
    // Store the analysis for future reference
    window.lastAnalysis = result;
}

// Initialize drag and drop styling
function initDragAndDropStyling() {
    const uploadBoxes = document.querySelectorAll('.upload-box');
    
    uploadBoxes.forEach(box => {
        box.addEventListener('dragover', (e) => {
            e.preventDefault();
            box.classList.add('drag-over');
        });
        
        box.addEventListener('dragleave', () => {
            box.classList.remove('drag-over');
        });
        
        box.addEventListener('drop', (e) => {
            e.preventDefault();
            box.classList.remove('drag-over');
        });
    });
}

// Show a standalone typing indicator in the chat
function showTypingIndicator() {
    const chatMessages = document.querySelector('.chat-messages');
    
    // Check if there's already a typing indicator
    if (document.querySelector('.typing-indicator-message')) {
        return;
    }
    
    const indicatorDiv = document.createElement('div');
    indicatorDiv.className = 'message ai-message typing-indicator-message';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    const typingDots = document.createElement('div');
    typingDots.className = 'typing-dots';
    
    // Create three dots for the typing animation
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        dot.className = 'dot';
        typingDots.appendChild(dot);
    }
    
    messageContent.appendChild(typingDots);
    indicatorDiv.appendChild(messageContent);
    chatMessages.appendChild(indicatorDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Remove the standalone typing indicator
function removeTypingIndicator() {
    const indicator = document.querySelector('.typing-indicator-message');
    if (indicator) {
        indicator.remove();
    }
}
