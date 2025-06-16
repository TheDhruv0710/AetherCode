// AetherCode - Main JavaScript File

document.addEventListener('DOMContentLoaded', () => {
    console.log('AetherCode initialized');
    
    // Tab Navigation
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');
    
    console.log('Tab links found:', tabLinks.length);
    console.log('Tab contents found:', tabContents.length);
    
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
            } else {
                console.error(`Tab content with id ${targetId} not found`);
            }
        });
    });
    
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
});
