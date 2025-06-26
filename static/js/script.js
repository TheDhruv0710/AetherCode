document.addEventListener('DOMContentLoaded', () => {
    // --- Constants ---
    const API_BASE_URL = 'http://127.0.0.1:5000/api';

    // --- DOM Elements ---
    const landingScreen = document.getElementById('landing-screen');
    const repoUrlInput = document.getElementById('repo-url');
    const analyzeBtn = document.getElementById('analyze-btn');
    const dashboard = document.getElementById('dashboard');
    const projectInfo = document.getElementById('project-info');
    const newAnalysisBtn = document.getElementById('new-analysis-btn');
    const exportBtn = document.getElementById('export-btn');
    const fileExplorer = document.getElementById('file-explorer');
    const codeViewer = document.getElementById('code-viewer');
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const techSpecModal = document.getElementById('tech-spec-modal');
    const techSpecContent = document.getElementById('tech-spec-content');
    const reportsModal = document.getElementById('reports-modal');
    const continueBtn = document.getElementById('continue-to-dashboard-btn');
    const reportsContent = document.getElementById('reports-content');
    const liveMinutes = document.getElementById('live-minutes');
    const todoList = document.getElementById('todo-list');

    // --- CodeMirror Initialization ---
    let codeEditor = null;
    
    // Initialize CodeMirror after DOM is loaded
    setTimeout(() => {
        const textarea = document.getElementById('code-editor');
        if (textarea) {
            codeEditor = CodeMirror.fromTextArea(textarea, {
                lineNumbers: true,
                mode: 'javascript',
                theme: 'material-darker',
                readOnly: true,
                lineWrapping: true,
                foldGutter: true,
                gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"]
            });
            codeEditor.setSize("100%", "100%");
        }
    }, 100);

    // --- State ---
    let currentProjectId = null;
    let currentRepoUrl = null;

    // --- Helper Functions ---
    async function handleApiError(response) {
        let errorMessage = `HTTP error! Status: ${response.status}`;
        try {
            const errorData = await response.json();
            errorMessage = errorData.error || 'An unknown error occurred.';
            if (errorData.details) {
                errorMessage += `\nDetails: ${errorData.details}`;
            }
        } catch (e) {
            // Response was not JSON or couldn't be parsed, use the default message
        }
        return errorMessage;
    }

    // --- Event Listeners ---
    analyzeBtn.addEventListener('click', handleRepoAnalysis);
    newAnalysisBtn.addEventListener('click', resetToLandingScreen);
    exportBtn.addEventListener('click', fetchAndShowReports);
    sendBtn.addEventListener('click', handleSendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSendMessage();
        }
    });

    // Modal event listeners
    continueBtn.addEventListener('click', () => {
        techSpecModal.style.display = 'none';
        showDashboard();
    });

    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        if (e.target === techSpecModal) {
            techSpecModal.style.display = 'none';
        }
        if (e.target === reportsModal) {
            reportsModal.style.display = 'none';
        }
    });

    // Close buttons
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const modal = e.target.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });

    // --- API & Core Functions ---
    async function handleRepoAnalysis() {
        const url = repoUrlInput.value.trim();
        if (!url) {
            alert('Please enter a GitHub repository URL.');
            return;
        }

        setLoading(analyzeBtn, 'Analyzing...', true);

        try {
            const response = await fetch(`${API_BASE_URL}/repo/analyze`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repo_url: url })
            });

            if (!response.ok) {
                const errorMessage = await handleApiError(response);
                throw new Error(errorMessage);
            }

            const data = await response.json();
            currentProjectId = data.project_id;
            currentRepoUrl = url;

            // Show animated greeting instead of tech spec modal
            showAnalysisGreeting(url.split('/').pop());

            // Update project info and file explorer
            projectInfo.textContent = `Project: ${url.split('/').pop()}`;
            if (data.files) {
                updateFileExplorer(data.files);
            }

        } catch (error) {
            console.error('Error analyzing repository:', error);
            alert(`Error analyzing repository: ${error.message}`);
        } finally {
            setLoading(analyzeBtn, 'Analyze', false);
        }
    }

    async function loadFileContent(path) {
        if (!currentProjectId) return;

        try {
            const response = await fetch(`${API_BASE_URL}/repo/${currentProjectId}/file?path=${encodeURIComponent(path)}`);
            
            if (!response.ok) {
                throw new Error(`Failed to load file: ${response.status}`);
            }

            const data = await response.json();
            showCode(data.content, path);

        } catch (error) {
            console.error('Error loading file:', error);
            showCode(`// Error loading file: ${error.message}`);
        }
    }

    async function handleSendMessage() {
        const message = userInput.value.trim();
        if (!message || !currentProjectId) return;

        displayUserMessage(message);
        userInput.value = '';
        setLoading(sendBtn, '', true);

        try {
            const thinkingId = addThinkingAnimation();
            await new Promise(resolve => setTimeout(resolve, 1000)); // Add a delay

            const response = await fetch(`${API_BASE_URL}/ai/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    project_id: currentProjectId,
                    message: message
                })
            });

            if (!response.ok) {
                const errorMessage = await handleApiError(response);
                throw new Error(errorMessage);
            }

            const data = await response.json();
            removeThinkingAnimation(thinkingId);
            displayAIMessage(data.response);

            // Update session notes if provided
            if (data.mom || data.insights) {
                updateSessionNotes(data.mom, data.insights);
            }

        } catch (error) {
            console.error('Error sending message:', error);
            displayAIMessage(`Error: ${error.message}`);
        } finally {
            setLoading(sendBtn, '', false);
        }
    }

    async function fetchAndShowReports() {
        if (!currentProjectId) {
            alert('No project selected.');
            return;
        }

        setLoading(exportBtn, 'Preparing Downloads...', true);

        try {
            // Show the reports modal with download options
            reportsContent.innerHTML = `
                <div class="reports-download-section">
                    <h3>📊 Available Reports</h3>
                    <p>Download individual reports or get all reports in a single ZIP file:</p>
                    
                    <div class="download-options">
                        <div class="individual-reports">
                            <h4>Individual Reports</h4>
                            <div class="download-buttons">
                                <button class="download-btn" onclick="window.downloadReport('tech_spec')">
                                    📋 Technical Specification
                                </button>
                                <button class="download-btn" onclick="window.downloadReport('code_health')">
                                    🏥 Code Health Report
                                </button>
                                <button class="download-btn" onclick="window.downloadReport('meeting_minutes')">
                                    📝 Meeting Minutes
                                </button>
                                <button class="download-btn" onclick="window.downloadReport('insights')">
                                    💡 Project Insights
                                </button>
                            </div>
                        </div>
                        
                        <div class="bulk-download">
                            <h4>Complete Package</h4>
                            <button class="download-btn primary" onclick="window.downloadAllReports()">
                                📦 Download All Reports (ZIP)
                            </button>
                        </div>
                    </div>
                    
                    <div class="download-info">
                        <p><strong>Note:</strong> Reports are generated specifically for the Python Calculator project and include calculator-focused analysis and recommendations.</p>
                    </div>
                </div>
            `;
            reportsModal.style.display = 'block';

        } catch (error) {
            console.error('Error preparing reports:', error);
            alert(`Error preparing reports: ${error.message}`);
        } finally {
            setLoading(exportBtn, 'Export Reports', false);
        }
    }

    // Download individual report
    window.downloadReport = async function(reportType) {
        if (!currentProjectId) {
            alert('No project selected.');
            return;
        }

        try {
            const downloadUrl = `${API_BASE_URL}/ai/reports/${currentProjectId}/download/${reportType}`;
            
            // Create a temporary link and trigger download
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = ''; // Let the server determine the filename
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
        } catch (error) {
            console.error('Error downloading report:', error);
            alert(`Error downloading report: ${error.message}`);
        }
    }

    // Download all reports as ZIP
    window.downloadAllReports = async function() {
        if (!currentProjectId) {
            alert('No project selected.');
            return;
        }

        try {
            const downloadUrl = `${API_BASE_URL}/ai/reports/${currentProjectId}/export`;
            
            // Create a temporary link and trigger download
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.download = ''; // Let the server determine the filename
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
        } catch (error) {
            console.error('Error downloading reports package:', error);
            alert(`Error downloading reports package: ${error.message}`);
        }
    }

    // --- UI Update Functions ---
    function showDashboard() {
        landingScreen.classList.add('hidden');
        dashboard.classList.remove('hidden');
    }

    function resetToLandingScreen() {
        dashboard.classList.add('hidden');
        landingScreen.classList.remove('hidden');
        
        // Reset state
        currentProjectId = null;
        currentRepoUrl = null;
        repoUrlInput.value = '';
        projectInfo.textContent = 'Project: Not Selected';
        chatContainer.innerHTML = '<div class="welcome-message"><p>Welcome to AetherCode! I\'ll analyze your code and ask relevant questions to help improve it.</p></div>';
        fileExplorer.innerHTML = '<div class="file-tree-placeholder">Repository files will appear here...</div>';
        codeViewer.innerHTML = '<pre><code>// Selected code will appear here</code></pre>';
        liveMinutes.innerHTML = '<p class="minutes-placeholder">Discussion points will appear as you chat with the AI...</p>';
        todoList.innerHTML = '<li class="todo-placeholder">Action items will be added here...</li>';
    }

    function displayUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.textContent = message;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function displayAIMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ai-message';
        messageDiv.textContent = message;
        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function updateFileExplorer(items) {
        fileExplorer.innerHTML = renderFileTree(items);
        addFileTreeEventListeners();
    }

    function updateSessionNotes(mom, insights) {
        if (mom) liveMinutes.innerHTML = `<p>${mom}</p>`;
        if (insights) {
            const todoItems = insights.split('\n').filter(item => item.trim());
            todoList.innerHTML = todoItems.map(item => `<li>${item}</li>`).join('');
        }
    }

    function showCode(codeSnippet, filePath = '') {
        if (codeEditor) {
            // Detect file type and set appropriate mode
            const mode = getCodeMirrorMode(filePath);
            codeEditor.setOption('mode', mode);
            codeEditor.setValue(codeSnippet);
            codeEditor.refresh();
        } else {
            // Fallback if CodeMirror isn't initialized yet
            codeViewer.innerHTML = `<pre><code>${codeSnippet}</code></pre>`;
        }
    }

    function getCodeMirrorMode(filePath) {
        const extension = filePath.split('.').pop().toLowerCase();
        
        const modeMap = {
            'js': 'javascript',
            'jsx': 'javascript',
            'ts': 'javascript',
            'tsx': 'javascript',
            'py': 'python',
            'html': 'htmlmixed',
            'htm': 'htmlmixed',
            'css': 'css',
            'scss': 'css',
            'sass': 'css',
            'less': 'css',
            'json': 'javascript',
            'xml': 'xml',
            'yaml': 'yaml',
            'yml': 'yaml',
            'md': 'markdown',
            'markdown': 'markdown',
            'sh': 'shell',
            'bash': 'shell',
            'zsh': 'shell',
            'fish': 'shell',
            'txt': 'text',
            'log': 'text',
            'cfg': 'text',
            'conf': 'text',
            'ini': 'text'
        };
        
        return modeMap[extension] || 'text';
    }

    function setLoading(button, text, isLoading = true) {
        if (isLoading) {
            button.disabled = true;
            button.classList.add('loading');
            if (text) button.textContent = text;
        } else {
            button.disabled = false;
            button.classList.remove('loading');
            if (text) button.textContent = text;
        }
    }

    // --- Render Functions ---
    function renderFileTree(items) {
        if (!items || items.length === 0) {
            return '<div class="file-tree-placeholder">No files found in repository.</div>';
        }

        return `<div class="file-tree">${items.map(item => renderFileItem(item)).join('')}</div>`;
    }

    function renderFileItem(item) {
        const isFolder = item.type === 'dir';
        const iconClass = getFileIconClass(item.name);
        const hasChildren = item.children && item.children.length > 0;

        return `
            <div class="file-item ${isFolder ? 'folder' : 'file'}" data-path="${item.path}" data-type="${item.type}">
                ${isFolder && hasChildren ? '<span class="folder-toggle"></span>' : '<span class="folder-toggle" style="visibility: hidden;"></span>'}
                <span class="file-icon ${iconClass}">
                    <i class="fas ${isFolder ? 'fa-folder' : getFileIcon(item.name)}"></i>
                </span>
                <span class="file-name">${item.name}</span>
            </div>
            ${hasChildren ? `<div class="file-children collapsed">${item.children.map(child => renderFileItem(child)).join('')}</div>` : ''}
        `;
    }

    function getFileIconClass(fileName) {
        const ext = fileName.split('.').pop().toLowerCase();
        const iconMap = {
            'js': 'javascript',
            'ts': 'typescript',
            'py': 'python',
            'css': 'css',
            'html': 'html',
            'htm': 'html',
            'json': 'json',
            'md': 'markdown',
            'txt': 'text',
            'png': 'image',
            'jpg': 'image',
            'jpeg': 'image',
            'gif': 'image',
            'svg': 'image'
        };
        return iconMap[ext] || 'text';
    }

    function getFileIcon(fileName) {
        const ext = fileName.split('.').pop().toLowerCase();
        const iconMap = {
            'js': 'fa-file-code',
            'ts': 'fa-file-code',
            'py': 'fa-file-code',
            'css': 'fa-file-code',
            'html': 'fa-file-code',
            'htm': 'fa-file-code',
            'json': 'fa-file-code',
            'md': 'fa-file-text',
            'txt': 'fa-file-text',
            'png': 'fa-file-image',
            'jpg': 'fa-file-image',
            'jpeg': 'fa-file-image',
            'gif': 'fa-file-image',
            'svg': 'fa-file-image'
        };
        return iconMap[ext] || 'fa-file';
    }

    function addFileTreeEventListeners() {
        // File/folder click handlers
        document.querySelectorAll('.file-item').forEach(item => {
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                
                // Remove previous selection
                document.querySelectorAll('.file-item.selected').forEach(selected => {
                    selected.classList.remove('selected');
                });
                
                // Add selection to clicked item
                item.classList.add('selected');
                
                const path = item.dataset.path;
                const type = item.dataset.type;
                
                if (type === 'file') {
                    loadFileContent(path);
                } else if (type === 'dir') {
                    // Toggle folder
                    const toggle = item.querySelector('.folder-toggle');
                    const children = item.nextElementSibling;
                    
                    if (children && children.classList.contains('file-children')) {
                        children.classList.toggle('collapsed');
                        toggle.classList.toggle('expanded');
                    }
                }
            });
        });

        // Folder toggle handlers
        document.querySelectorAll('.folder-toggle').forEach(toggle => {
            toggle.addEventListener('click', (e) => {
                e.stopPropagation();
                const item = toggle.closest('.file-item');
                const children = item.nextElementSibling;
                
                if (children && children.classList.contains('file-children')) {
                    children.classList.toggle('collapsed');
                    toggle.classList.toggle('expanded');
                }
            });
        });
    }

    function addThinkingAnimation() {
        const thinkingId = 'thinking-' + Date.now();
        const thinkingDiv = document.createElement('div');
        thinkingDiv.id = thinkingId;
        thinkingDiv.className = 'message assistant-message thinking-animation';
        thinkingDiv.innerHTML = `
            <div class="thinking-content">
                <div class="thinking-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <span class="thinking-text">Analyzing your question...</span>
            </div>
        `;
        
        chatContainer.appendChild(thinkingDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        return thinkingId;
    }

    function removeThinkingAnimation(thinkingId) {
        const thinkingElement = document.getElementById(thinkingId);
        if (thinkingElement) {
            thinkingElement.remove();
        }
    }

    function showAnalysisGreeting(projectName) {
        // Create animated greeting overlay
        const greetingOverlay = document.createElement('div');
        greetingOverlay.className = 'greeting-overlay';
        greetingOverlay.innerHTML = `
            <div class="greeting-container">
                <div class="greeting-icon">
                    <div class="digital-core-greeting">
                        <div class="core-ring ring-1"></div>
                        <div class="core-ring ring-2"></div>
                        <div class="core-ring ring-3"></div>
                        <div class="core-center">⚡</div>
                    </div>
                </div>
                <div class="greeting-content">
                    <h1 class="greeting-title">Repository Analysis Complete!</h1>
                    <div class="greeting-subtitle">
                        <span class="project-label">Project:</span>
                        <span class="project-name">${projectName}</span>
                    </div>
                    <div class="greeting-message">
                        <p>✨ Code structure analyzed</p>
                        <p>🔍 Files indexed and ready</p>
                        <p>🤖 AI assistant initialized</p>
                    </div>
                    <div class="greeting-action">
                        <p>Ready to start your code review session!</p>
                        <div class="greeting-progress">
                            <div class="progress-bar"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(greetingOverlay);
        
        // Animate the greeting sequence
        setTimeout(() => {
            greetingOverlay.classList.add('show');
        }, 100);
        
        // Auto-dismiss after 4 seconds and show dashboard
        setTimeout(() => {
            greetingOverlay.classList.add('fade-out');
            setTimeout(() => {
                document.body.removeChild(greetingOverlay);
                showDashboard();
                
                // Add welcome message to chat
                addWelcomeMessage(projectName);
            }, 800);
        }, 4000);
    }

    function addWelcomeMessage(projectName) {
        const welcomeDiv = document.createElement('div');
        welcomeDiv.className = 'message assistant-message welcome-message';
        welcomeDiv.innerHTML = `
            <div class="message-content">
                <h3>🎉 Welcome to your ${projectName} code review session!</h3>
                <p>I've successfully analyzed your repository and I'm ready to help you improve your code. Here's what we can explore together:</p>
                <ul>
                    <li>📋 <strong>Code Structure</strong> - Discuss architecture and organization</li>
                    <li>🛡️ <strong>Error Handling</strong> - Review exception management</li>
                    <li>🧪 <strong>Testing Strategy</strong> - Plan comprehensive test coverage</li>
                    <li>🚀 <strong>Improvements</strong> - Identify enhancement opportunities</li>
                    <li>📚 <strong>Documentation</strong> - Enhance code documentation</li>
                </ul>
                <p><strong>💡 Try asking:</strong> "Hello, can you analyze this?" or "Tell me about the code structure"</p>
            </div>
        `;
        
        chatContainer.appendChild(welcomeDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
