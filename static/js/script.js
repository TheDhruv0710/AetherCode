// AetherCode - Main JavaScript File

document.addEventListener('DOMContentLoaded', () => {
    console.log('AetherCode initialized');
    
    // Tab Navigation
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');
    
    console.log('Tab links found:', tabLinks.length);
    console.log('Tab contents found:', tabContents.length);
    
    // Log all tab links and their data-tab attributes
    tabLinks.forEach(link => {
        console.log('Tab link:', link.textContent.trim(), 'data-tab:', link.getAttribute('data-tab'));
    });
    
    // Log all tab content sections and their IDs
    tabContents.forEach(content => {
        console.log('Tab content:', content.id);
    });
    
    // Add click event listeners to tab links
    tabLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('data-tab');
            console.log('Tab clicked:', targetId);
            
            // Hide all tab contents
            tabContents.forEach(content => {
                content.classList.remove('active');
                console.log('Removed active class from:', content.id);
            });
            
            // Remove active class from all tab links
            tabLinks.forEach(tabLink => {
                tabLink.classList.remove('active');
            });
            
            // Show the target tab content
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.classList.add('active');
                console.log('Added active class to:', targetId);
                
                // Add active class to the clicked tab link
                link.classList.add('active');
                
                // Initialize specific tab content if needed
                if (targetId === 'tech-spec') {
                    console.log('Initializing tech-spec tab');
                    initTechSpecTab();
                } else if (targetId === 'test-cases') {
                    console.log('Initializing test-cases tab');
                    initTestCasesTab();
                }
            } else {
                console.error(`Tab content with id ${targetId} not found`);
            }
        });
    });
    
    // Initialize Tech Spec tab functionality
    function initTechSpecTab() {
        const generateSpecBtn = document.getElementById('generate-spec');
        if (generateSpecBtn) {
            if (!generateSpecBtn.hasEventListener) {
                generateSpecBtn.addEventListener('click', () => {
                    console.log('Generate spec button clicked');
                    generateTechSpec();
                });
                generateSpecBtn.hasEventListener = true;
            }
        } else {
            console.error('Generate spec button not found');
        }
    }
    
    // Generate technical specification
    function generateTechSpec() {
        const projectDescription = document.getElementById('project-description');
        if (!projectDescription || !projectDescription.value.trim()) {
            alert('Please enter a project description first.');
            return;
        }
        
        const description = projectDescription.value.trim();
        const outputFormat = document.getElementById('output-format').value;
        
        // Get selected sections
        const selectedSections = [];
        document.querySelectorAll('input[name="spec-section"]:checked').forEach(checkbox => {
            selectedSections.push(checkbox.value);
        });
        
        // Show loading state
        const generatedSpec = document.getElementById('generated-spec');
        if (generatedSpec) {
            generatedSpec.innerHTML = '<div class="loading-message"><i class="fas fa-spinner fa-spin"></i><p>Generating specification...</p></div>';
        }
        
        // Call API to generate spec
        fetch('/api/generate-documentation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                description,
                outputFormat,
                sections: selectedSections
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                generatedSpec.innerHTML = `<div class="error-message"><p>Error: ${escapeHtml(data.error)}</p></div>`;
                return;
            }
            
            // Display generated spec
            if (outputFormat === 'markdown') {
                generatedSpec.innerHTML = `<pre class="markdown-content">${escapeHtml(data.content)}</pre>`;
            } else {
                generatedSpec.innerHTML = `<pre>${escapeHtml(data.content)}</pre>`;
            }
            
            // Enable download button
            const downloadSpecBtn = document.getElementById('download-spec');
            if (downloadSpecBtn) {
                downloadSpecBtn.disabled = false;
                if (!downloadSpecBtn.hasEventListener) {
                    downloadSpecBtn.addEventListener('click', () => {
                        downloadSpec(data.content, outputFormat);
                    });
                    downloadSpecBtn.hasEventListener = true;
                }
            }
        })
        .catch(error => {
            console.error('Error generating spec:', error);
            generatedSpec.innerHTML = `<div class="error-message"><p>Error connecting to server. Please try again.</p></div>`;
        });
    }
    
    // Initialize Test Cases tab functionality
    function initTestCasesTab() {
        const generateTestsBtn = document.getElementById('generate-tests');
        if (generateTestsBtn) {
            if (!generateTestsBtn.hasEventListener) {
                generateTestsBtn.addEventListener('click', () => {
                    console.log('Generate tests button clicked');
                    generateTestCases();
                });
                generateTestsBtn.hasEventListener = true;
            }
        } else {
            console.error('Generate tests button not found');
        }
    }
    
    // Generate test cases
    function generateTestCases() {
        // Get the code editor content
        const editor = document.querySelector('.CodeMirror');
        if (!editor || !editor.CodeMirror) {
            alert('Please write some code in the editor first.');
            return;
        }
        
        const code = editor.CodeMirror.getValue();
        const language = document.getElementById('language-select')?.value || 'javascript';
        const testFramework = document.getElementById('test-framework')?.value || 'jest';
        
        // Show loading state
        const generatedTests = document.getElementById('generated-tests');
        if (generatedTests) {
            generatedTests.innerHTML = '<div class="loading-message"><i class="fas fa-spinner fa-spin"></i><p>Generating tests...</p></div>';
        }
        
        // Call API to generate tests
        fetch('/api/generate-tests', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code,
                language,
                framework: testFramework
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                generatedTests.innerHTML = `<div class="error-message"><p>Error: ${escapeHtml(data.error)}</p></div>`;
                return;
            }
            
            // Display generated tests
            generatedTests.innerHTML = `<pre class="code-content">${escapeHtml(data.tests)}</pre>`;
            
            // Enable copy button
            const copyTestsBtn = document.getElementById('copy-tests');
            if (copyTestsBtn) {
                copyTestsBtn.disabled = false;
                if (!copyTestsBtn.hasEventListener) {
                    copyTestsBtn.addEventListener('click', () => {
                        copyToClipboard(data.tests);
                        alert('Tests copied to clipboard!');
                    });
                    copyTestsBtn.hasEventListener = true;
                }
            }
        })
        .catch(error => {
            console.error('Error generating tests:', error);
            generatedTests.innerHTML = `<div class="error-message"><p>Error connecting to server. Please try again.</p></div>`;
        });
    }
    
    // Helper function to copy text to clipboard
    function copyToClipboard(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
    }
    
    // Initialize CodeMirror for main editor
    const codeEditorElement = document.getElementById('code-editor');
    if (codeEditorElement) {
        console.log('Initializing CodeMirror editor');
        const editor = CodeMirror(codeEditorElement, {
            mode: 'javascript',
            theme: 'dracula',
            lineNumbers: true,
            autoCloseBrackets: true,
            matchBrackets: true,
            indentUnit: 4,
            tabSize: 4,
            lineWrapping: true
        });
        
        // Set initial content
        editor.setValue('// Start coding here\nconsole.log("Hello, AetherCode!");\n');
        
        // Language selector functionality
        const languageSelect = document.getElementById('language-select');
        if (languageSelect) {
            languageSelect.addEventListener('change', () => {
                const language = languageSelect.value;
                updateEditorMode(editor, language);
            });
        }
    } else {
        console.error('Code editor element not found');
    }
    
    // Helper function to update editor mode
    function updateEditorMode(editor, language) {
        let mode;
        switch (language) {
            case 'javascript':
                mode = 'javascript';
                break;
            case 'python':
                mode = 'python';
                break;
            case 'java':
                mode = 'text/x-java';
                break;
            case 'csharp':
                mode = 'text/x-csharp';
                break;
            case 'cpp':
                mode = 'text/x-c++src';
                break;
            case 'php':
                mode = 'application/x-httpd-php';
                break;
            case 'ruby':
                mode = 'ruby';
                break;
            case 'go':
                mode = 'go';
                break;
            case 'rust':
                mode = 'rust';
                break;
            default:
                mode = 'javascript';
        }
        editor.setOption('mode', mode);
        console.log('Editor mode updated to:', mode);
    }
    
    // Add run code functionality
    const runCodeBtn = document.getElementById('run-code');
    if (runCodeBtn && codeEditorElement) {
        const editor = document.querySelector('.CodeMirror').CodeMirror;
        const outputDisplay = document.getElementById('output-display');
        const executionStatus = document.getElementById('execution-status');
        const executionTime = document.getElementById('execution-time');
        
        runCodeBtn.addEventListener('click', () => {
            const code = editor.getValue();
            const languageSelect = document.getElementById('language-select');
            const language = languageSelect ? languageSelect.value : 'javascript';
            
            // Update status
            if (executionStatus) executionStatus.textContent = 'Running...';
            if (executionTime) executionTime.textContent = '';
            
            const startTime = performance.now();
            
            // Call the backend API to execute the code
            fetch('/api/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code, language }),
            })
            .then(response => response.json())
            .then(data => {
                const endTime = performance.now();
                const duration = ((endTime - startTime) / 1000).toFixed(2);
                
                if (outputDisplay) {
                    if (data.error) {
                        outputDisplay.innerHTML = `<pre class="output-content error">${escapeHtml(data.error)}</pre>`;
                    } else {
                        outputDisplay.innerHTML = `<pre class="output-content">${escapeHtml(data.output)}</pre>`;
                    }
                }
                
                // Update status
                if (executionStatus) executionStatus.textContent = data.error ? 'Error' : 'Completed';
                if (executionTime) executionTime.textContent = `${duration}s`;
            })
            .catch(error => {
                console.error('Error executing code:', error);
                if (outputDisplay) {
                    outputDisplay.innerHTML = `<pre class="output-content error">Error connecting to server: ${escapeHtml(error.message)}</pre>`;
                }
                if (executionStatus) executionStatus.textContent = 'Error';
            });
        });
    }
    
    // Add chat functionality
    const chatInput = document.getElementById('chat-input');
    const sendMessageBtn = document.getElementById('send-message');
    const chatMessages = document.getElementById('chat-messages');
    
    console.log('Chat elements:', {
        chatInput: !!chatInput,
        sendMessageBtn: !!sendMessageBtn,
        chatMessages: !!chatMessages
    });
    
    if (chatInput && sendMessageBtn && chatMessages) {
        sendMessageBtn.addEventListener('click', () => {
            console.log('Send message button clicked');
            sendMessage();
        });
        
        chatInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                console.log('Enter key pressed in chat input');
                sendMessage();
            }
        });
        
        function sendMessage() {
            const message = chatInput.value.trim();
            if (!message) {
                console.log('Empty message, not sending');
                return;
            }
            
            console.log('Sending message:', message);
            
            // Add user message to chat
            addMessageToChat('user', message);
            chatInput.value = '';
            
            // Show typing indicator
            const typingIndicator = document.createElement('div');
            typingIndicator.className = 'message ai-message typing';
            typingIndicator.innerHTML = '<div class="message-content"><p>Typing<span class="typing-dots">...</span></p></div>';
            chatMessages.appendChild(typingIndicator);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Call the backend API
            console.log('Calling chat API endpoint');
            fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            })
            .then(response => {
                console.log('Chat API response status:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('Chat API response data:', data);
                // Remove typing indicator
                chatMessages.removeChild(typingIndicator);
                
                // Add AI response to chat
                if (data.response) {
                    addMessageToChat('ai', data.response);
                } else if (data.error) {
                    addMessageToChat('ai', `Error: ${data.error}`);
                } else {
                    addMessageToChat('ai', 'Received empty response from server');
                }
            })
            .catch(error => {
                console.error('Error sending message:', error);
                try {
                    chatMessages.removeChild(typingIndicator);
                } catch (e) {
                    console.error('Error removing typing indicator:', e);
                }
                addMessageToChat('ai', 'Sorry, I encountered an error. Please try again.');
            });
        }
        
        function addMessageToChat(sender, message) {
            console.log('Adding message to chat:', { sender, message });
            const messageElement = document.createElement('div');
            messageElement.className = `message ${sender}-message`;
            messageElement.innerHTML = `<div class="message-content"><p>${escapeHtml(message)}</p></div>`;
            chatMessages.appendChild(messageElement);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
    } else {
        console.error('Chat elements not found:', {
            chatInput: !!chatInput,
            sendMessageBtn: !!sendMessageBtn,
            chatMessages: !!chatMessages
        });
    }
    
    // Add code review functionality
    const reviewCodeBtn = document.getElementById('review-code');
    
    if (reviewCodeBtn && codeEditorElement) {
        const editor = document.querySelector('.CodeMirror').CodeMirror;
        
        reviewCodeBtn.addEventListener('click', () => {
            const code = editor.getValue();
            const languageSelect = document.getElementById('language-select');
            const language = languageSelect ? languageSelect.value : 'javascript';
            
            // Show loading state
            const reportPlaceholder = document.querySelector('.report-placeholder');
            const reportContent = document.querySelector('.report-content');
            
            if (reportPlaceholder && reportContent) {
                reportPlaceholder.style.display = 'none';
                reportContent.style.display = 'block';
                document.getElementById('report-generation-date').textContent = new Date().toLocaleString();
                document.getElementById('overall-review-message').textContent = 'Analyzing your code...';
                document.getElementById('health-summary').textContent = 'In progress';
                document.getElementById('health-score').textContent = '...';
                document.getElementById('issues-list').innerHTML = '<div class="loading-message"><i class="fas fa-spinner fa-spin"></i><p>Generating code review...</p></div>';
            }
            
            // Call the backend API
            fetch('/api/review', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code, language }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error reviewing code:', data.error);
                    return;
                }
                
                // Update the report with the review results
                document.getElementById('overall-review-message').textContent = data.summary || 'Code review completed.';
                document.getElementById('health-summary').textContent = data.health || 'Good';
                document.getElementById('health-score').textContent = data.score || '7/10';
                
                // Display issues
                const issuesList = document.getElementById('issues-list');
                issuesList.innerHTML = '';
                
                if (data.issues && data.issues.length > 0) {
                    data.issues.forEach(issue => {
                        const issueItem = document.createElement('div');
                        issueItem.className = 'issue-item';
                        issueItem.innerHTML = `
                            <div class="issue-header">
                                <span class="issue-type ${issue.type.toLowerCase()}">${issue.type}</span>
                                <span class="issue-severity ${issue.severity.toLowerCase()}">${issue.severity}</span>
                            </div>
                            <div class="issue-description">
                                <p>${escapeHtml(issue.description)}</p>
                            </div>
                            <div class="issue-location">
                                <span class="issue-line">Line: ${issue.line || 'N/A'}</span>
                            </div>
                        `;
                        issuesList.appendChild(issueItem);
                    });
                } else {
                    issuesList.innerHTML = '<p>No issues found. Great job!</p>';
                }
            })
            .catch(error => {
                console.error('Error reviewing code:', error);
                document.getElementById('overall-review-message').textContent = 'Error generating code review.';
            });
        });
    }
    
    // Helper function to escape HTML
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
