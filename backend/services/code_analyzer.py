"""
Code Analyzer Service for AetherCode

This service analyzes code and provides feedback, suggestions, and insights.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger(__name__)

class CodeAnalyzer:
    """
    Analyzes code for quality, patterns, and potential issues.
    """
    
    def __init__(self):
        """Initialize the code analyzer with language-specific rules"""
        self.language_extensions = {
            # JavaScript and TypeScript
            'js': 'javascript',
            'jsx': 'javascript',
            'ts': 'typescript',
            'tsx': 'typescript',
            
            # Python
            'py': 'python',
            'pyc': 'python',
            'pyd': 'python',
            'pyo': 'python',
            'pyw': 'python',
            
            # Java
            'java': 'java',
            
            # C#
            'cs': 'csharp',
            
            # C++
            'cpp': 'cpp',
            'cc': 'cpp',
            'cxx': 'cpp',
            'c': 'cpp',
            'h': 'cpp',
            'hpp': 'cpp',
            
            # PHP
            'php': 'php',
            
            # Ruby
            'rb': 'ruby',
            
            # Go
            'go': 'go',
            
            # Swift
            'swift': 'swift',
            
            # Kotlin
            'kt': 'kotlin',
            'kts': 'kotlin',
            
            # Rust
            'rs': 'rust',
            
            # HTML
            'html': 'html',
            'htm': 'html',
            
            # CSS
            'css': 'css',
            
            # SQL
            'sql': 'sql'
        }
        
        # Initialize language-specific analyzers
        self._init_analyzers()
        
    def _init_analyzers(self):
        """Initialize language-specific analyzers"""
        self.analyzers = {
            'javascript': self._analyze_javascript,
            'typescript': self._analyze_javascript,  # Reuse JS analyzer for now
            'python': self._analyze_python,
            'java': self._analyze_java,
            'csharp': self._analyze_csharp,
            'cpp': self._analyze_cpp,
            'php': self._analyze_php,
            'ruby': self._analyze_ruby,
            'go': self._analyze_go,
            'swift': self._analyze_swift,
            'kotlin': self._analyze_kotlin,
            'rust': self._analyze_rust,
            'html': self._analyze_html,
            'css': self._analyze_css,
            'sql': self._analyze_sql
        }
        
    def detect_language(self, extension: str) -> str:
        """
        Detect programming language from file extension
        
        Args:
            extension: File extension without the dot
            
        Returns:
            Detected language or 'javascript' as default
        """
        return self.language_extensions.get(extension, 'javascript')
        
    def analyze(self, code: str, language: str, filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze code and provide feedback
        
        Args:
            code: Source code to analyze
            language: Programming language
            filename: Optional filename
            
        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Analyzing {language} code")
        
        # Basic code metrics
        metrics = self._calculate_metrics(code)
        
        # Language-specific analysis
        analyzer = self.analyzers.get(language, self._analyze_generic)
        language_analysis = analyzer(code)
        
        # Combine results
        result = {
            "metrics": metrics,
            "language": language,
            "filename": filename,
            "analysis": language_analysis
        }
        
        return result
        
    def analyze_project(self, file_analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze an entire project based on individual file analyses
        
        Args:
            file_analyses: List of file analysis results
            
        Returns:
            Project-level analysis
        """
        # Count files by language
        language_counts = {}
        total_lines = 0
        total_code_lines = 0
        total_comment_lines = 0
        total_issues = 0
        
        for file_analysis in file_analyses:
            if "error" in file_analysis:
                continue
                
            lang = file_analysis.get("language", "unknown")
            language_counts[lang] = language_counts.get(lang, 0) + 1
            
            # Aggregate metrics
            metrics = file_analysis.get("analysis", {}).get("metrics", {})
            total_lines += metrics.get("total_lines", 0)
            total_code_lines += metrics.get("code_lines", 0)
            total_comment_lines += metrics.get("comment_lines", 0)
            
            # Count issues
            issues = file_analysis.get("analysis", {}).get("issues", [])
            total_issues += len(issues)
        
        # Calculate project summary
        primary_language = max(language_counts.items(), key=lambda x: x[1])[0] if language_counts else "unknown"
        
        return {
            "file_count": len(file_analyses),
            "language_distribution": language_counts,
            "primary_language": primary_language,
            "total_lines": total_lines,
            "total_code_lines": total_code_lines,
            "total_comment_lines": total_comment_lines,
            "comment_ratio": round(total_comment_lines / total_code_lines * 100, 2) if total_code_lines > 0 else 0,
            "total_issues": total_issues,
            "overall_health": self._calculate_health_score(total_issues, total_code_lines)
        }
    
    def _calculate_health_score(self, issues: int, code_lines: int) -> str:
        """Calculate overall health score based on issues per line of code"""
        if code_lines == 0:
            return "Unknown"
            
        issue_density = issues / code_lines
        
        if issue_density < 0.01:
            return "Excellent"
        elif issue_density < 0.03:
            return "Good"
        elif issue_density < 0.05:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _calculate_metrics(self, code: str) -> Dict[str, int]:
        """
        Calculate basic code metrics
        
        Args:
            code: Source code
            
        Returns:
            Dictionary with metrics
        """
        lines = code.split('\n')
        total_lines = len(lines)
        
        # Count empty lines
        empty_lines = sum(1 for line in lines if line.strip() == '')
        
        # Approximate comment lines (this is a simple heuristic)
        comment_lines = 0
        in_multiline_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            # Check for multiline comments
            if '/*' in stripped and '*/' in stripped:
                comment_lines += 1
                continue
                
            if '/*' in stripped:
                in_multiline_comment = True
                comment_lines += 1
                continue
                
            if '*/' in stripped:
                in_multiline_comment = False
                comment_lines += 1
                continue
                
            if in_multiline_comment:
                comment_lines += 1
                continue
                
            # Check for single-line comments
            if stripped.startswith('//') or stripped.startswith('#') or stripped.startswith('--'):
                comment_lines += 1
        
        # Calculate code lines
        code_lines = total_lines - empty_lines - comment_lines
        
        return {
            "total_lines": total_lines,
            "code_lines": code_lines,
            "comment_lines": comment_lines,
            "empty_lines": empty_lines,
            "comment_ratio": round(comment_lines / code_lines * 100, 2) if code_lines > 0 else 0
        }
    
    def _analyze_generic(self, code: str) -> Dict[str, Any]:
        """
        Generic code analysis for unsupported languages
        
        Args:
            code: Source code
            
        Returns:
            Analysis results
        """
        return {
            "issues": [],
            "suggestions": [
                "Consider adding more comments to explain complex logic",
                "Ensure consistent formatting throughout the code"
            ],
            "insights": [
                "This language doesn't have specific analysis rules implemented yet"
            ]
        }
    
    def _analyze_javascript(self, code: str) -> Dict[str, Any]:
        """
        Analyze JavaScript/TypeScript code
        
        Args:
            code: Source code
            
        Returns:
            Analysis results
        """
        issues = []
        suggestions = []
        insights = []
        
        # Check for console.log statements
        console_logs = len(re.findall(r'console\.log\s*\(', code))
        if console_logs > 0:
            issues.append({
                "type": "debugging_code",
                "message": f"Found {console_logs} console.log statement(s) that should be removed in production code",
                "severity": "warning"
            })
        
        # Check for var usage (prefer let/const)
        var_usage = len(re.findall(r'\bvar\s+', code))
        if var_usage > 0:
            suggestions.append("Consider using 'let' and 'const' instead of 'var' for better scoping")
        
        # Check for potential memory leaks in event listeners
        event_listeners = len(re.findall(r'addEventListener\s*\(', code))
        remove_listeners = len(re.findall(r'removeEventListener\s*\(', code))
        if event_listeners > remove_listeners:
            issues.append({
                "type": "potential_memory_leak",
                "message": "Potential memory leak: more addEventListener calls than removeEventListener",
                "severity": "warning"
            })
        
        # Check for error handling
        try_blocks = len(re.findall(r'\btry\s*{', code))
        if try_blocks == 0 and len(code) > 500:
            suggestions.append("Consider adding error handling with try/catch blocks for robust code")
        
        # Check for modern JS features
        if 'async' in code and 'await' in code:
            insights.append("Code uses modern async/await pattern for asynchronous operations")
        
        if '=>' in code:
            insights.append("Code uses arrow functions, a modern JavaScript feature")
        
        # Check for potential security issues
        if 'eval(' in code:
            issues.append({
                "type": "security_risk",
                "message": "Usage of eval() can introduce security vulnerabilities",
                "severity": "critical"
            })
        
        if 'innerHTML' in code:
            issues.append({
                "type": "security_risk",
                "message": "Usage of innerHTML can lead to XSS vulnerabilities if not properly sanitized",
                "severity": "warning"
            })
        
        return {
            "issues": issues,
            "suggestions": suggestions,
            "insights": insights
        }
    
    def _analyze_python(self, code: str) -> Dict[str, Any]:
        """
        Analyze Python code
        
        Args:
            code: Source code
            
        Returns:
            Analysis results
        """
        issues = []
        suggestions = []
        insights = []
        
        # Check for print statements (should use logging in production)
        print_statements = len(re.findall(r'\bprint\s*\(', code))
        if print_statements > 0:
            issues.append({
                "type": "debugging_code",
                "message": f"Found {print_statements} print statement(s) that should be replaced with proper logging in production code",
                "severity": "info"
            })
        
        # Check for exception handling
        try_blocks = len(re.findall(r'\btry\s*:', code))
        except_blocks = len(re.findall(r'\bexcept\s*', code))
        if try_blocks > 0 and try_blocks == except_blocks and 'Exception:' in code:
            issues.append({
                "type": "broad_exception",
                "message": "Catching broad Exception is not recommended. Catch specific exceptions instead.",
                "severity": "warning"
            })
        
        # Check for PEP8 compliance (very basic)
        lines = code.split('\n')
        long_lines = sum(1 for line in lines if len(line) > 79)
        if long_lines > 0:
            suggestions.append(f"Found {long_lines} lines longer than 79 characters (PEP8 recommendation)")
        
        # Check for imports
        if 'import *' in code:
            issues.append({
                "type": "wildcard_import",
                "message": "Wildcard imports (import *) are not recommended as they make code less readable",
                "severity": "warning"
            })
        
        # Check for modern Python features
        if 'async def' in code:
            insights.append("Code uses async/await pattern for asynchronous operations")
        
        if any(('f"' in line or "f'" in line) for line in lines):
            insights.append("Code uses f-strings, a modern Python 3.6+ feature")
        
        # Check for potential security issues
        if 'eval(' in code or 'exec(' in code:
            issues.append({
                "type": "security_risk",
                "message": "Usage of eval() or exec() can introduce security vulnerabilities",
                "severity": "critical"
            })
        
        return {
            "issues": issues,
            "suggestions": suggestions,
            "insights": insights
        }
    
    def _analyze_java(self, code: str) -> Dict[str, Any]:
        """Analyze Java code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_csharp(self, code: str) -> Dict[str, Any]:
        """Analyze C# code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_cpp(self, code: str) -> Dict[str, Any]:
        """Analyze C++ code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_php(self, code: str) -> Dict[str, Any]:
        """Analyze PHP code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_ruby(self, code: str) -> Dict[str, Any]:
        """Analyze Ruby code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_go(self, code: str) -> Dict[str, Any]:
        """Analyze Go code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_swift(self, code: str) -> Dict[str, Any]:
        """Analyze Swift code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_kotlin(self, code: str) -> Dict[str, Any]:
        """Analyze Kotlin code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_rust(self, code: str) -> Dict[str, Any]:
        """Analyze Rust code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_html(self, code: str) -> Dict[str, Any]:
        """Analyze HTML code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_css(self, code: str) -> Dict[str, Any]:
        """Analyze CSS code"""
        # Basic implementation for now
        return self._analyze_generic(code)
    
    def _analyze_sql(self, code: str) -> Dict[str, Any]:
        """Analyze SQL code"""
        # Basic implementation for now
        return self._analyze_generic(code)
