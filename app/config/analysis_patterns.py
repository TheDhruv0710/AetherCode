"""
Code analysis patterns for AetherCode application
"""

# Code Analysis Patterns
CODE_ANALYSIS_PATTERNS = {
    'python': {
        'complexity': r'def\s+\w+\s*\([^)]*\):\s*(?:\n\s+.*){10,}',
        'unused_import': r'import\s+(\w+)(?!.*\1)',
        'bad_practice': r'except:',
    },
    'javascript': {
        'complexity': r'function\s+\w+\s*\([^)]*\)\s*{(?:\n.*){10,}}',
        'unused_var': r'(const|let|var)\s+(\w+)(?!.*\2)',
        'bad_practice': r'==(?!=)',
    },
    'general': {
        'long_line': r'.{100,}',
        'todo': r'TODO|FIXME',
    }
}
