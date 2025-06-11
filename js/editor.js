/**
 * AetherCode - CodeMirror Editor Implementation
 */

// Global editor instance that will be accessible across files
window.editor = null;

// Debug flag
const DEBUG = true;

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM content loaded - initializing editor');
    
    const editorContainer = document.getElementById('code-mirror-editor');
    if (!editorContainer) {
        console.error('Editor container not found!');
        return;
    }
    
    const languageSelect = document.getElementById('language-select');
    if (!languageSelect) {
        console.error('Language select not found!');
    }
    
    const clearBtn = document.getElementById('clear-btn');
    if (!clearBtn) {
        console.error('Clear button not found!');
    }
    
    const formatBtn = document.getElementById('format-btn');
    if (!formatBtn) {
        console.error('Format button not found!');
    }
    
    // Initialize CodeMirror editor
    try {
        initCodeMirror();
        console.log('CodeMirror initialized successfully:', window.editor);
    } catch (error) {
        console.error('Error initializing CodeMirror:', error);
    }
    
    // Clear button functionality
    clearBtn.addEventListener('click', () => {
        window.editor.setValue('');
        window.editor.focus();
    });
    
    // Format button functionality
    formatBtn.addEventListener('click', () => {
        formatCode();
    });
    
    // Language selection functionality
    languageSelect.addEventListener('change', () => {
        updateEditorMode();
    });
    
    // Set initial language from dropdown
    updateEditorMode();
    
    // Initialize file upload functionality
    initFileUploads();
});

/**
 * Initialize the CodeMirror editor
 */
function initCodeMirror() {
    console.log('Initializing CodeMirror editor...');
    const editorContainer = document.getElementById('code-mirror-editor');
    
    if (!editorContainer) {
        console.error('Editor container element not found!');
        return;
    }
    
    if (typeof CodeMirror === 'undefined') {
        console.error('CodeMirror is not defined! Check if the library is loaded.');
        return;
    }
    
    // Clear any existing content in the container
    editorContainer.innerHTML = '';
    
    console.log('Creating CodeMirror instance...');
    
    // Create CodeMirror instance
    try {
        window.editor = CodeMirror(editorContainer, {
            lineNumbers: true,
            theme: 'dracula',
            mode: 'javascript', // Default mode
            indentUnit: 4,
            smartIndent: true,
            tabSize: 4,
            indentWithTabs: false,
            lineWrapping: false,
            matchBrackets: true,
            autoCloseBrackets: true,
            styleActiveLine: true,
            foldGutter: true,
            gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
            extraKeys: {
                'Ctrl-Space': 'autocomplete',
                'Ctrl-Q': function(cm) { cm.foldCode(cm.getCursor()); },
                'Ctrl-/': 'toggleComment',
                'Ctrl-F': function() { formatCode(); }
            }
        });
        console.log('CodeMirror instance created successfully');
    } catch (error) {
        console.error('Error creating CodeMirror instance:', error);
    }
    
    // Set initial placeholder
    if (window.editor) {
        window.editor.setValue('// Start coding here...');
        window.editor.clearHistory(); // Clear undo history for initial content
    }
    
    // Update editor header with current language
    updateEditorHeader();
}

/**
 * Update the editor header with the current language
 */
function updateEditorHeader() {
    const languageSelect = document.getElementById('language-select');
    if (!languageSelect) return;
    
    const language = languageSelect.value;
    const editorTitle = document.querySelector('.editor-header h2');
    
    if (editorTitle) {
        // Capitalize first letter of language
        const displayLang = language.charAt(0).toUpperCase() + language.slice(1);
        editorTitle.textContent = `Code Editor (${displayLang})`;
    } else {
        console.error('Editor title element not found');
    }
}

/**
 * Update the editor mode based on the selected language
 */
function updateEditorMode() {
    const languageSelect = document.getElementById('language-select');
    const language = languageSelect.value;
    
    // Map language values to CodeMirror modes
    let mode;
    switch (language) {
        case 'javascript':
            mode = 'javascript';
            break;
        case 'python':
            mode = 'python';
            break;
        case 'java':
        case 'csharp':
        case 'cpp':
            mode = 'clike';
            break;
        case 'php':
            mode = 'php';
            break;
        case 'ruby':
            mode = 'ruby';
            break;
        case 'go':
            mode = 'go';
            break;
        case 'swift':
            mode = 'swift';
            break;
        case 'rust':
            mode = 'rust';
            break;
        case 'html':
            mode = 'htmlmixed';
            break;
        case 'css':
            mode = 'css';
            break;
        case 'sql':
            mode = 'sql';
            break;
        case 'typescript':
            mode = 'javascript';
            break;
        default:
            mode = 'javascript';
    }
    
    // Set editor mode
    if (window.editor) {
        window.editor.setOption('mode', mode);
        
        // Update editor header with current language
        updateEditorHeader();
    }
    
    // Add a subtle notification in the chat if there's code in the editor
    if (window.editor && window.editor.getValue().trim() !== '' && window.addAIMessage) {
        if (window.showTypingIndicator) window.showTypingIndicator();
        setTimeout(() => {
            if (window.removeTypingIndicator) window.removeTypingIndicator();
            if (window.addAIMessage) {
                window.addAIMessage(`I see you're working with ${languageSelect.options[languageSelect.selectedIndex].text}. Let me know if you need any specific help with this language.`);
            }
        }, 1000);
    }
}

/**
 * Update the editor header with the current language
 */
function updateEditorHeader() {
    const languageSelect = document.getElementById('language-select');
    const editorHeader = document.querySelector('.editor-header h2');
    if (editorHeader) {
        editorHeader.textContent = `Code Editor (${languageSelect.options[languageSelect.selectedIndex].text})`;
    }
}

/**
 * Format the code in the editor based on the selected language
 */
function formatCode() {
    const code = window.editor.getValue();
    const language = document.getElementById('language-select').value;
    let formattedCode = code;
    
    try {
        switch(language) {
            case 'javascript':
            case 'typescript':
                formattedCode = js_beautify(code, {
                    indent_size: 4,
                    space_in_empty_paren: true
                });
                break;
            case 'html':
                formattedCode = html_beautify(code, {
                    indent_size: 4,
                    max_preserve_newlines: 1
                });
                break;
            case 'css':
                formattedCode = css_beautify(code, {
                    indent_size: 4
                });
                break;
            case 'python':
                formattedCode = formatPython(code);
                break;
            default:
                formattedCode = basicFormatting(code);
        }
        
        // Update editor with formatted code
        window.editor.setValue(formattedCode);
        
        // Flash animation to indicate formatting
        const editorElement = document.querySelector('.CodeMirror');
        editorElement.classList.add('flash');
        setTimeout(() => {
            editorElement.classList.remove('flash');
        }, 300);
        
        // Show success message
        const languageSelect = document.getElementById('language-select');
        if (window.addAIMessage) {
            window.showTypingIndicator && window.showTypingIndicator();
            setTimeout(() => {
                window.removeTypingIndicator && window.removeTypingIndicator();
                window.addAIMessage(`Code formatted successfully using ${languageSelect.options[languageSelect.selectedIndex].text} formatting rules.`);
            }, 500);
        }
        
    } catch (error) {
        console.error('Formatting error:', error);
        window.addAIMessage(`Sorry, I encountered an error while formatting your ${languageSelect.options[languageSelect.selectedIndex].text} code.`);
    }
}

/**
 * Basic formatting for languages without specific formatters
 */
function basicFormatting(code) {
    // This is a very simplified formatter that just ensures consistent indentation
    // In a real app, you would use language-specific libraries
    return code;
}

/**
 * Simple Python formatter (basic indentation)
 */
function formatPython(code) {
    // This is a very simplified Python formatter
    // In a real app, you would use a proper Python formatter like Black or YAPF
    return code;
}

// Initialize file upload functionality
function initFileUploads() {
    const singleFileUpload = document.getElementById('single-file-upload');
    const projectUpload = document.getElementById('project-upload');
    const codeFileInput = document.getElementById('code-file-input');
    const projectFilesInput = document.getElementById('project-files-input');
    const languageSelect = document.getElementById('language-select');
    
    // Highlight drop area when dragging over
    [singleFileUpload, projectUpload].forEach(uploadArea => {
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
        });
    });
    
    // Handle single file upload
    codeFileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        // Detect language from file extension and set dropdown
        const fileExtension = getFileExtension(file.name);
        const detectedLanguage = detectLanguageFromExtension(fileExtension);
        
        if (detectedLanguage) {
            languageSelect.value = detectedLanguage;
            updateEditorMode(); // Update editor mode based on selected language
        }
        
        const reader = new FileReader();
        reader.onload = (event) => {
            // Set code in CodeMirror editor
            if (window.editor) {
                window.editor.setValue(event.target.result);
                window.editor.refresh();
            } else {
                console.error('Editor not initialized!');
            }
            
            // Show success message in chat
            const langName = languageSelect.options[languageSelect.selectedIndex].text;
            window.addAIMessage(`File "${file.name}" loaded successfully. I've detected it as a ${langName} file. You can now submit it for review or make edits.`);
        };
        
        reader.onerror = () => {
            window.addAIMessage(`Error reading file "${file.name}". Please try again.`);
        };
        
        reader.readAsText(file);
    });
    
    // Handle project files upload
    projectFilesInput.addEventListener('change', (e) => {
        const files = e.target.files;
        if (files.length === 0) return;
        
        let fileNames = [];
        for (let i = 0; i < Math.min(files.length, 5); i++) {
            fileNames.push(files[i].name);
        }
        
        if (files.length > 5) {
            fileNames.push(`and ${files.length - 5} more files`);
        }
        
        window.addAIMessage(`Project files selected: ${fileNames.join(', ')}. Click "Submit Code for Review" to analyze these files.`);
    });
    
    // Enable drag and drop directly on the editor
    const codeMirrorElement = document.querySelector('.CodeMirror');
    if (codeMirrorElement) {
        codeMirrorElement.addEventListener('dragover', (e) => {
            e.preventDefault();
            codeMirrorElement.classList.add('drag-over');
        });
        
        codeMirrorElement.addEventListener('dragleave', () => {
            codeMirrorElement.classList.remove('drag-over');
        });
        
        codeMirrorElement.addEventListener('drop', (e) => {
            e.preventDefault();
            codeMirrorElement.classList.remove('drag-over');
            
            // Handle dropped files
            if (e.dataTransfer.files.length > 0) {
                const file = e.dataTransfer.files[0];
                
                // Detect language from file extension and set dropdown
                const fileExtension = getFileExtension(file.name);
                const detectedLanguage = detectLanguageFromExtension(fileExtension);
                
                if (detectedLanguage) {
                    languageSelect.value = detectedLanguage;
                    updateEditorMode();
                }
                
                const reader = new FileReader();
                reader.onload = (event) => {
                    editor.setValue(event.target.result);
                    editor.refresh();
                    
                    // Show success message in chat
                    const langName = languageSelect.options[languageSelect.selectedIndex].text;
                    window.addAIMessage(`File "${file.name}" dropped into editor. I've detected it as a ${langName} file.`);
                };
                
                reader.readAsText(file);
            }
        });
    }
}

// Get file extension from filename
function getFileExtension(filename) {
    return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2).toLowerCase();
}

// Detect programming language from file extension
function detectLanguageFromExtension(extension) {
    const extensionMap = {
        // JavaScript and TypeScript
        'js': 'javascript',
        'jsx': 'javascript',
        'ts': 'typescript',
        'tsx': 'typescript',
        
        // Python
        'py': 'python',
        'pyc': 'python',
        'pyd': 'python',
        'pyo': 'python',
        'pyw': 'python',
        
        // Java
        'java': 'java',
        
        // C#
        'cs': 'csharp',
        
        // C++
        'cpp': 'cpp',
        'cc': 'cpp',
        'cxx': 'cpp',
        'c': 'cpp',
        'h': 'cpp',
        'hpp': 'cpp',
        
        // PHP
        'php': 'php',
        
        // Ruby
        'rb': 'ruby',
        
        // Go
        'go': 'go',
        
        // Swift
        'swift': 'swift',
        
        // Kotlin
        'kt': 'kotlin',
        'kts': 'kotlin',
        
        // Rust
        'rs': 'rust',
        
        // HTML
        'html': 'html',
        'htm': 'html',
        
        // CSS
        'css': 'css',
        
        // SQL
        'sql': 'sql'
    };
    
    return extensionMap[extension] || null;
}

// Get the current code from the editor
window.getEditorCode = function() {
    return window.editor ? window.editor.getValue() : '';
};

// Set code in the editor
window.setEditorCode = function(code) {
    if (window.editor) {
        window.editor.setValue(code);
        window.editor.refresh();
    }
};

// Get the current selected language
window.getSelectedLanguage = function() {
    const languageSelect = document.getElementById('language-select');
    return languageSelect ? languageSelect.value : 'javascript';
};

// Get the current selected language display name
window.getSelectedLanguageDisplayName = function() {
    const languageSelect = document.getElementById('language-select');
    return languageSelect ? languageSelect.options[languageSelect.selectedIndex].text : 'JavaScript';
};
