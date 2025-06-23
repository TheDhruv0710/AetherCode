document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements - Landing Screen
    const landingScreen = document.getElementById('landing-screen');
    const repoUrlInput = document.getElementById('repo-url');
    const analyzeBtn = document.getElementById('analyze-btn');
    
    // DOM Elements - Dashboard
    const dashboard = document.getElementById('dashboard');
    const projectInfo = document.getElementById('project-info');
    const newAnalysisBtn = document.getElementById('new-analysis-btn');
    const exportBtn = document.getElementById('export-btn');
    const fileExplorer = document.getElementById('file-explorer');
    const codeViewer = document.getElementById('code-viewer');
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const liveMinutes = document.getElementById('live-minutes');
    const todoList = document.getElementById('todo-list');
    
    // DOM Elements - Modals
    const techSpecModal = document.getElementById('tech-spec-modal');
    const reportsModal = document.getElementById('reports-modal');
    const continueBtn = document.getElementById('continue-to-dashboard-btn');
    const digitalCore = document.getElementById('digital-core');
    const closeBtns = document.querySelectorAll('.close-btn');
    const reportsContent = document.getElementById('reports-content');

    // State variables
    let currentProjectId = null;
    let currentRepoUrl = null;
    let questions = [];
    let currentQuestionIndex = 0;
    let dialogueHistory = [];

    // Initialize and animate the digital core
    function initDigitalCore() {
        // Create data streams
        createDataStreams();
        
        // Periodically create new data streams
        setInterval(createDataStreams, 3000);
        
        // Add click interaction
        digitalCore.addEventListener('click', intensifyCore);
    }
    
    // Create data stream elements
    function createDataStreams() {
        // Clear existing streams that have completed their animation
        const existingStreams = digitalCore.querySelectorAll('.data-stream');
        existingStreams.forEach(stream => {
            if (stream.getAttribute('data-complete') === 'true') {
                stream.remove();
            }
        });
        
        // Create 3-5 new data streams
        const numStreams = Math.floor(Math.random() * 3) + 3;
        
        for (let i = 0; i < numStreams; i++) {
            const stream = document.createElement('div');
            stream.className = 'data-stream';
            
            // Random positioning
            const angle = Math.random() * 360;
            const distance = 30 + Math.random() * 25; // Distance from center
            
            const x = Math.cos(angle * Math.PI / 180) * distance;
            const y = Math.sin(angle * Math.PI / 180) * distance;
            
            // Set styles
            stream.style.left = `calc(50% + ${x}px)`;
            stream.style.top = `calc(50% + ${y}px)`;
            stream.style.height = `${10 + Math.random() * 15}px`;
            stream.style.transform = `rotate(${angle}deg)`;
            stream.style.animationDuration = `${1 + Math.random() * 2}s`;
            stream.style.opacity = `${0.3 + Math.random() * 0.4}`;
            
            // Mark for removal after animation completes
            stream.addEventListener('animationend', () => {
                stream.setAttribute('data-complete', 'true');
            });
            
            digitalCore.appendChild(stream);
        }
    }
    
    // Intensify the digital core animation
    function intensifyCore() {
        digitalCore.classList.add('intensified');
        
        // Create extra data streams during intensified state
        const numExtraStreams = Math.floor(Math.random() * 5) + 5;
        for (let i = 0; i < numExtraStreams; i++) {
            const stream = document.createElement('div');
            stream.className = 'data-stream';
            
            // Random positioning for extra streams
            const angle = Math.random() * 360;
            const distance = 20 + Math.random() * 40;
            
            const x = Math.cos(angle * Math.PI / 180) * distance;
            const y = Math.sin(angle * Math.PI / 180) * distance;
            
            stream.style.left = `calc(50% + ${x}px)`;
            stream.style.top = `calc(50% + ${y}px)`;
            stream.style.height = `${15 + Math.random() * 20}px`;
            stream.style.transform = `rotate(${angle}deg)`;
            stream.style.animationDuration = `${0.5 + Math.random()}s`;
            stream.style.opacity = `${0.5 + Math.random() * 0.5}`;
            
            stream.addEventListener('animationend', () => {
                stream.remove();
            });
            
            digitalCore.appendChild(stream);
        }
        
        setTimeout(() => {
            digitalCore.classList.remove('intensified');
        }, 3000);
    }

    // Display AI message with typing effect
    function displayAIMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'ai-message';
        chatContainer.appendChild(messageElement);

        let i = 0;
        const typingEffect = setInterval(() => {
            if (i < message.length) {
                messageElement.textContent += message.charAt(i);
                i++;
                chatContainer.scrollTop = chatContainer.scrollHeight;
            } else {
                clearInterval(typingEffect);
            }
        }, 30);
    }

    // Display user message
    function displayUserMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = 'user-message';
        messageElement.textContent = message;
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Show code in the code viewer
    function showCode(codeSnippet, highlightedLines) {
        codeViewer.innerHTML = `<pre><code>${codeSnippet}</code></pre>`;
        // In a real implementation, you would use a library like highlight.js
        // to add syntax highlighting and line highlighting
    }

    // Ask the next question in the dialogue
    function askNextQuestion() {
        if (currentQuestionIndex < questions.length) {
            const question = questions[currentQuestionIndex];
            displayAIMessage(question);
            
            // Mock code snippet related to the question
            const mockCodeSnippet = `function example() {
  // This is a sample code snippet
  console.log("Hello, world!");
  return true;
}`;
            
            showCode(mockCodeSnippet, [2, 3]);
            currentQuestionIndex++;
        } else {
            // No more questions, show the reports
            displayAIMessage("Thank you for your insights. I've compiled the reports based on our discussion.");
            setTimeout(showReports, 2000);
        }
    }

    // Show the final reports
    async function showReports() {
        try {
            const response = await fetch(`/api/get_reports?project_id=${currentProjectId}`);
            const data = await response.json();
            
            // Format the reports
            let reportsHTML = `
                <div class="report-section">
                    <h3>Technical Specification</h3>
                    <p>${data.tech_spec}</p>
                </div>
                <div class="report-section">
                    <h3>Minutes of Meeting</h3>
                    <p>${data.mom}</p>
                </div>
                <div class="report-section">
                    <h3>Relevant Insights</h3>
                    <p>${data.insights}</p>
                </div>
                <div class="report-section">
                    <h3>Code Health Report</h3>
                    <p>${data.code_health}</p>
                </div>
                <button id="download-btn" class="download-btn">Download Reports</button>
            `;
            
            reportsContent.innerHTML = reportsHTML;
            
            // Hide dialogue modal and show reports modal
            dialogueModal.style.display = 'none';
            reportsModal.style.display = 'block';
            
            // Add event listener for download button
            document.getElementById('download-btn').addEventListener('click', () => {
                alert('Reports downloaded successfully!');
            });
        } catch (error) {
            console.error('Error fetching reports:', error);
        }
    }

    // Function to show dashboard and hide landing screen
    function showDashboard() {
        landingScreen.classList.add('hidden');
        dashboard.classList.remove('hidden');
        projectInfo.textContent = `Project: ${currentRepoUrl}`;
        
        // Update file explorer with mock data for now
        updateFileExplorer();
    }
    
    // Function to reset to landing screen
    function resetToLandingScreen() {
        dashboard.classList.add('hidden');
        landingScreen.classList.remove('hidden');
        repoUrlInput.value = '';
        resetState();
    }
    
    // Reset all state variables
    function resetState() {
        currentProjectId = null;
        currentRepoUrl = null;
        questions = [];
        currentQuestionIndex = 0;
        dialogueHistory = [];
        todoItems = [];
        
        // Reset UI elements
        chatContainer.innerHTML = '<div class="welcome-message"><p>Welcome to AetherCode! I\'ll analyze your code and ask relevant questions to help improve it.</p></div>';
        fileExplorer.innerHTML = '<div class="file-tree-placeholder">Repository files will appear here...</div>';
        codeViewer.innerHTML = '<pre><code>// Selected code will appear here</code></pre>';
        liveMinutes.innerHTML = '<p class="minutes-placeholder">Minutes will appear as you chat with the AI...</p>';
        todoList.innerHTML = '<li class="todo-placeholder">To-Do items will be added here...</li>';
    }
    
    // Update file explorer with repository structure
    async function updateFileExplorer() {
        try {
            // Fetch the actual repository structure from the backend
            const response = await fetch(`/api/repo_structure?project_id=${currentProjectId}`);
            const data = await response.json();
            
            console.log('Repository structure response:', data);
            
            if (data.error) {
                console.error('Error fetching repository structure:', data.error);
                fileExplorer.innerHTML = `<div class="file-tree-placeholder">Error loading repository structure: ${data.error}</div>`;
                return;
            }
            
            if (!data.file_structure || data.file_structure === "Repository structure not available.") {
                fileExplorer.innerHTML = '<div class="file-tree-placeholder">Repository structure not available. The repository may still be downloading or processing.</div>';
                return;
            }
            
            // Parse the file structure string into a hierarchical object
            const fileStructure = parseFileStructure(data.file_structure);
            
            // Render the file tree
            fileExplorer.innerHTML = renderFileTree(fileStructure);
            
            // Add click event listeners to folders and files
            addFileTreeEventListeners();
        } catch (error) {
            console.error('Error updating file explorer:', error);
            fileExplorer.innerHTML = '<div class="file-tree-placeholder">Error loading repository structure. Please try again later.</div>';
        }
    }
    
    // Add event listeners to the file tree elements
    function addFileTreeEventListeners() {
        // Add click event listeners to folders
        document.querySelectorAll('.folder-name').forEach(folderElement => {
            folderElement.addEventListener('click', function() {
                // Toggle the folder's expanded state
                const folderItem = this.parentElement;
                folderItem.classList.toggle('expanded');
                
                // Toggle visibility of child elements
                const childList = folderItem.querySelector('ul');
                if (childList) {
                    childList.style.display = folderItem.classList.contains('expanded') ? 'block' : 'none';
                }
            });
        });
        
        // Add click event listeners to files
        document.querySelectorAll('.file-name').forEach(item => {
            item.addEventListener('click', function() {
                const path = this.getAttribute('data-path');
                console.log('File clicked:', path);
                // Here you would typically load the file content
                // For now, just update the selected file in the UI
                document.querySelectorAll('.file-name').forEach(f => f.classList.remove('selected'));
                this.classList.add('selected');
                
                // Update the code viewer with a placeholder message
                const codeViewer = document.getElementById('code-viewer');
                if (codeViewer) {
                    codeViewer.innerHTML = `<div class="code-placeholder">Loading file: ${path}...</div>`;
                }
            });
        });
        
        // Add click event listeners to folders
        document.querySelectorAll('.folder-item').forEach(item => {
            item.addEventListener('click', function() {
                this.classList.toggle('expanded');
                const childrenContainer = this.nextElementSibling;
                childrenContainer.style.display = childrenContainer.style.display === 'none' ? 'block' : 'none';
            });
        });
    }
    
    // Parse file structure string into a hierarchical object
    function parseFileStructure(fileStructureString) {
        if (!fileStructureString || typeof fileStructureString !== 'string') {
            console.error('Invalid file structure:', fileStructureString);
            return [];
        }
        
        // Log the file structure for debugging
        console.log('File structure string:', fileStructureString);
        
        // Check if the first line is "Repository structure:" and remove it
        const lines = fileStructureString.split('\n')
            .filter(line => line.trim() !== '')
            .filter((line, index) => index !== 0 || !line.includes('Repository structure:'));
        
        // Root object to hold the file structure
        const root = [];
        
        // Stack to keep track of the current path and indentation level
        const stack = [{ items: root, level: -1 }];
        
        // Current path to build full file paths
        let currentPath = '';
        
        // Process each line
        lines.forEach(line => {
            // Count the indentation level (number of spaces at the beginning)
            const match = line.match(/^(\s*)(.+)$/);
            if (!match) return;
            
            const indent = match[1].length;
            const name = match[2].trim();
            
            // Skip "more files" lines
            if (name.includes('(more files)') || name.includes('(more files not shown)')) {
                return;
            }
            
            // Determine if it's a file or folder based on the presence of a trailing slash
            const isFolder = name.endsWith('/');
            const cleanName = isFolder ? name.replace(/\/$/, '') : name;
            
            // Find the parent at the appropriate indentation level
            while (stack.length > 1 && stack[stack.length - 1].level >= indent) {
                stack.pop();
                // Update current path when going up in the hierarchy
                const pathParts = currentPath.split('/');
                pathParts.pop();
                currentPath = pathParts.join('/');
            }
            
            const parent = stack[stack.length - 1].items;
            
            if (isFolder) {
                // Update current path
                currentPath = currentPath ? `${currentPath}/${cleanName}` : cleanName;
                
                // Create a new folder item
                const folder = {
                    name: cleanName,
                    type: 'folder',
                    children: []
                };
                parent.push(folder);
                
                // Add this folder to the stack
                stack.push({
                    items: folder.children,
                    level: indent
                });
            } else {
                // Create a new file item with full path
                const filePath = currentPath ? `${currentPath}/${cleanName}` : cleanName;
                parent.push({
                    name: cleanName,
                    type: 'file',
                    path: `/${filePath}`
                });
            }
        });
        
        return root;
    }
    
    // Render file tree as HTML
    function renderFileTree(items) {
        if (!items || items.length === 0) {
            return '<div class="file-tree-placeholder">No files to display</div>';
        }
        
        let html = '<ul class="file-tree">';
        
        // Sort items: folders first, then files, both alphabetically
        const sortedItems = [...items].sort((a, b) => {
            if (a.type !== b.type) {
                return a.type === 'folder' ? -1 : 1; // Folders before files
            }
            return a.name.localeCompare(b.name); // Alphabetical within same type
        });
        
        sortedItems.forEach(item => {
            if (item.type === 'folder') {
                html += `
                    <li class="folder">
                        <span class="folder-name" title="${item.name}">
                            <i class="fas fa-folder"></i> ${item.name}
                        </span>
                        ${renderFileTree(item.children)}
                    </li>
                `;
            } else {
                // Determine file icon based on extension
                const extension = item.name.split('.').pop().toLowerCase();
                let iconClass = 'fas fa-file';
                
                // Add specific icons for common file types
                if (['js', 'jsx', 'ts', 'tsx'].includes(extension)) {
                    iconClass = 'fab fa-js';
                } else if (['py'].includes(extension)) {
                    iconClass = 'fab fa-python';
                } else if (['html', 'htm'].includes(extension)) {
                    iconClass = 'fab fa-html5';
                } else if (['css', 'scss', 'sass'].includes(extension)) {
                    iconClass = 'fab fa-css3-alt';
                } else if (['md', 'markdown'].includes(extension)) {
                    iconClass = 'fas fa-file-alt';
                } else if (['json'].includes(extension)) {
                    iconClass = 'fas fa-code';
                }
                
                html += `
                    <li class="file">
                        <span class="file-name" data-path="${item.path}" title="${item.path}">
                            <i class="${iconClass}"></i> ${item.name}
                        </span>
                    </li>
                `;
            }
        });
        
        html += '</ul>';
        return html;
    }
    
    // Load file content
    function loadFileContent(path) {
        // Mock file content for demo
        const mockContent = `// This is a mock content for ${path}
// In a real implementation, this would fetch the actual file content

function exampleCode() {
  console.log("This is a sample code from the selected file");
  return true;
}`;
        
        codeViewer.innerHTML = `<pre><code>${mockContent}</code></pre>`;
    }

    // Event Listeners
    analyzeBtn.addEventListener('click', async () => {
        const repoUrl = repoUrlInput.value;
        if (!repoUrl) {
            alert('Please enter a GitHub repository URL.');
            return;
        }

        // Store the repo URL
        currentRepoUrl = repoUrl;
        
        // Intensify the landing page core
        const landingCore = document.getElementById('landing-digital-core');
        landingCore.classList.add('intensified');
        
        try {
            const response = await fetch('/api/analyze_repo', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ repo_url: repoUrl })
            });

            const data = await response.json();
            
            currentProjectId = 'project_' + Date.now();
            
            document.getElementById('tech-spec-content').innerHTML = data.tech_spec;
            techSpecModal.style.display = 'block';
            
            questions = data.questions || [];
            
            // Remove the intensified effect
            setTimeout(() => {
                landingCore.classList.remove('intensified');
            }, 3000);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while analyzing the repository.');
            landingCore.classList.remove('intensified');
        }
    });
    
    // Continue to dashboard button
    continueBtn.addEventListener('click', () => {
        techSpecModal.style.display = 'none';
        showDashboard();
        if (questions.length > 0) {
            askNextQuestion();
        }
    });
    
    // New analysis button
    newAnalysisBtn.addEventListener('click', () => {
        resetToLandingScreen();
    });
    
    // Export button
    exportBtn.addEventListener('click', () => {
        fetchAndShowReports();
    });
    
    // Send button for chat
    sendBtn.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message) {
            displayUserMessage(message);
            userInput.value = '';
            
            // Add to dialogue history
            dialogueHistory.push({ role: 'user', content: message });
            
            // Process the dialogue
            processTurn(message);
        }
    });
    
    // Allow sending message with Enter key
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendBtn.click();
        }
    });
    
    // Close buttons for modals
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.modal');
            if (modal) {
                modal.style.display = 'none';
            }
        });
    });
    
    // Process a dialogue turn
    async function processTurn(userMessage) {
        try {
            const response = await fetch('/api/dialogue_turn', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    project_id: currentProjectId,
                    user_message: userMessage,
                    dialogue_history: dialogueHistory
                })
            });
            
            const data = await response.json();
            
            // Add AI response to dialogue history
            dialogueHistory.push({ role: 'assistant', content: data.ai_response });
            
            // Update code viewer with relevant code
            if (data.code_snippet) {
                loadFileContent(data.code_snippet.path, data.code_snippet.content);
            }
            
            // Display AI response
            displayAIMessage(data.ai_response);
            
            // Update minutes
            updateMinutes(userMessage, data.ai_response);
            
            // Extract and add to-dos if any
            if (data.todos && data.todos.length > 0) {
                addTodos(data.todos);
            }
            
            // If this was the last question, prepare to show reports
            if (currentQuestionIndex >= questions.length) {
                setTimeout(() => {
                    displayAIMessage("Thank you for your insights. I've compiled the reports based on our discussion.");
                    setTimeout(fetchAndShowReports, 2000);
                }, 1000);
            } else {
                // Otherwise, ask the next question after a short delay
                setTimeout(askNextQuestion, 1000);
            }
        } catch (error) {
            console.error('Error processing dialogue turn:', error);
            displayAIMessage("I'm sorry, there was an error processing your response. Let's continue with the next question.");
            setTimeout(askNextQuestion, 1000);
        }
    }
    
    // Update minutes with conversation
    function updateMinutes(userMessage, aiResponse) {
        const minutesPlaceholder = document.querySelector('.minutes-placeholder');
        if (minutesPlaceholder) {
            minutesPlaceholder.remove();
        }
        
        const minuteEntry = document.createElement('div');
        minuteEntry.className = 'minute-entry';
        minuteEntry.innerHTML = `
            <p class="timestamp">${new Date().toLocaleTimeString()}</p>
            <p class="minute-ai"><strong>AI:</strong> ${aiResponse}</p>
            <p class="minute-user"><strong>User:</strong> ${userMessage}</p>
            <hr>
        `;
        
        liveMinutes.appendChild(minuteEntry);
        liveMinutes.scrollTop = liveMinutes.scrollHeight;
    }
    
    // Add to-dos to the list
    function addTodos(todos) {
        const todoPlaceholder = document.querySelector('.todo-placeholder');
        if (todoPlaceholder) {
            todoPlaceholder.remove();
        }
        
        todos.forEach(todo => {
            const todoItem = document.createElement('li');
            todoItem.className = 'todo-item';
            todoItem.innerHTML = `
                <input type="checkbox" id="todo-${Date.now()}-${Math.random().toString(36).substr(2, 5)}">
                <span>${todo}</span>
            `;
            
            todoList.appendChild(todoItem);
            
            // Add event listener for checkbox
            const checkbox = todoItem.querySelector('input[type="checkbox"]');
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    todoItem.classList.add('completed');
                } else {
                    todoItem.classList.remove('completed');
                }
            });
        });
    }
    
    // Fetch and show reports
    async function fetchAndShowReports() {
        try {
            const response = await fetch(`/api/get_reports?project_id=${currentProjectId}`);
            const data = await response.json();
            
            // Format the reports
            let reportsHTML = `
                <div class="report-section">
                    <h3>Technical Specification</h3>
                    <p>${data.tech_spec}</p>
                </div>
                <div class="report-section">
                    <h3>Minutes of Meeting</h3>
                    <p>${data.mom}</p>
                </div>
                <div class="report-section">
                    <h3>Relevant Insights</h3>
                    <p>${data.insights}</p>
                </div>
                <div class="report-section">
                    <h3>Code Health Report</h3>
                    <p>${data.code_health}</p>
                </div>
                <button id="download-btn" class="download-btn">Download Reports</button>
            `;
            
            reportsContent.innerHTML = reportsHTML;
            reportsModal.style.display = 'block';
            
            // Add download button event listener
            document.getElementById('download-btn').addEventListener('click', () => {
                alert('Reports would be downloaded here in a real implementation.');
            });
        } catch (error) {
            console.error('Error fetching reports:', error);
            alert('An error occurred while fetching the reports.');
        }
    }
    
    // Initialize the digital core animation
    initDigitalCore();
    
    // Add click event to the landing page digital core as well
    const landingCore = document.getElementById('landing-digital-core');
    if (landingCore) {
        // Create initial data streams for landing core
        createDataStreams.call(landingCore);
        
        // Add click interaction to landing core
        landingCore.addEventListener('click', () => {
            landingCore.classList.add('intensified');
            
            // Create extra data streams during intensified state
            const numExtraStreams = Math.floor(Math.random() * 5) + 5;
            for (let i = 0; i < numExtraStreams; i++) {
                const stream = document.createElement('div');
                stream.className = 'data-stream';
                
                // Random positioning for extra streams
                const angle = Math.random() * 360;
                const distance = 20 + Math.random() * 40;
                
                const x = Math.cos(angle * Math.PI / 180) * distance;
                const y = Math.sin(angle * Math.PI / 180) * distance;
                
                stream.style.left = `calc(50% + ${x}px)`;
                stream.style.top = `calc(50% + ${y}px)`;
                stream.style.height = `${15 + Math.random() * 20}px`;
                stream.style.transform = `rotate(${angle}deg)`;
                stream.style.animationDuration = `${0.5 + Math.random()}s`;
                stream.style.opacity = `${0.5 + Math.random() * 0.5}`;
                
                stream.addEventListener('animationend', () => {
                    stream.remove();
                });
                
                landingCore.appendChild(stream);
            }
            
            setTimeout(() => {
                landingCore.classList.remove('intensified');
            }, 3000);
        });
    }
});