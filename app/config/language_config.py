"""
Language configuration settings for AetherCode application
"""

# Language configurations
LANGUAGE_CONFIGS = {
    'python': {
        'extension': '.py',
        'command': 'python',
        'timeout': 10
    },
    'javascript': {
        'extension': '.js',
        'command': 'node',
        'timeout': 10
    },
    'java': {
        'extension': '.java',
        'command': 'java',
        'compile_command': 'javac',
        'timeout': 15,
        'main_class': 'Main'
    },
    'csharp': {
        'extension': '.cs',
        'command': 'dotnet run',
        'timeout': 15
    },
    'cpp': {
        'extension': '.cpp',
        'command': './a.out',
        'compile_command': 'g++',
        'timeout': 10
    },
    'ruby': {
        'extension': '.rb',
        'command': 'ruby',
        'timeout': 10
    },
    'go': {
        'extension': '.go',
        'command': 'go run',
        'timeout': 10
    },
    'rust': {
        'extension': '.rs',
        'command': './main',
        'compile_command': 'rustc',
        'timeout': 15
    },
    'php': {
        'extension': '.php',
        'command': 'php',
        'timeout': 10
    }
}
