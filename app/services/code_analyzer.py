"""
Code analysis service for AetherCode application
"""
import re
from app.config.analysis_patterns import CODE_ANALYSIS_PATTERNS

def analyze_code(code, language):
    """Analyze code for potential issues and patterns"""
    results = {
        'issues': [],
        'metrics': {
            'lines': len(code.split('\n')),
            'characters': len(code),
        }
    }
    
    # Get patterns for the specific language or use general patterns
    patterns = CODE_ANALYSIS_PATTERNS.get(language, {})
    patterns.update(CODE_ANALYSIS_PATTERNS['general'])
    
    # Check for patterns
    for issue_type, pattern in patterns.items():
        matches = re.finditer(pattern, code)
        for match in matches:
            line_number = code[:match.start()].count('\n') + 1
            results['issues'].append({
                'type': issue_type,
                'line': line_number,
                'text': match.group(0)[:50] + ('...' if len(match.group(0)) > 50 else '')
            })
    
    # Calculate complexity metrics
    results['metrics']['complexity'] = estimate_complexity(code, language)
    
    return results

def estimate_complexity(code, language):
    """Estimate code complexity based on language-specific heuristics"""
    # This is a simplified complexity estimation
    # In a real implementation, we would use language-specific tools
    
    if language == 'python':
        # Count control structures
        control_structures = len(re.findall(r'\b(if|for|while|def)\b', code))
        nested_structures = len(re.findall(r'\n\s{4,}(if|for|while)', code))
    elif language in ['javascript', 'java', 'csharp', 'cpp']:
        # Count control structures
        control_structures = len(re.findall(r'\b(if|for|while|function|class)\b', code))
        nested_structures = len(re.findall(r'[{]\s*\n.*\n.*\s*[{]', code, re.DOTALL))
    else:
        # Generic estimation
        control_structures = len(re.findall(r'\b(if|for|while)\b', code))
        nested_structures = 0
    
    # Simple complexity score
    return control_structures + nested_structures * 2

def get_language_from_extension(extension):
    """Determine language from file extension"""
    extension_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.java': 'java',
        '.cs': 'csharp',
        '.cpp': 'cpp',
        '.c': 'cpp',
        '.rb': 'ruby',
        '.go': 'go',
        '.rs': 'rust',
        '.php': 'php',
        '.ts': 'typescript'
    }
    
    return extension_map.get(extension, 'unknown')
