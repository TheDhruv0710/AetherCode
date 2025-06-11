"""
Code Executor Service for AetherCode

This service executes code in various programming languages and returns the output.
"""

import os
import subprocess
import tempfile
import logging
import time
import json
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class CodeExecutor:
    """
    Executes code in various programming languages and returns the output.
    """
    
    def __init__(self):
        """Initialize the code executor with language-specific execution commands"""
        self.execution_configs = {
            'javascript': {
                'extension': 'js',
                'command': 'node',
                'timeout': 10,
                'setup': None
            },
            'python': {
                'extension': 'py',
                'command': 'python',
                'timeout': 10,
                'setup': None
            },
            'java': {
                'extension': 'java',
                'command': 'java',
                'timeout': 15,
                'setup': self._setup_java
            },
            'cpp': {
                'extension': 'cpp',
                'command': None,  # Will be determined by setup function
                'timeout': 10,
                'setup': self._setup_cpp
            },
            'csharp': {
                'extension': 'cs',
                'command': 'dotnet',
                'timeout': 15,
                'setup': self._setup_csharp
            },
            'ruby': {
                'extension': 'rb',
                'command': 'ruby',
                'timeout': 10,
                'setup': None
            },
            'go': {
                'extension': 'go',
                'command': 'go',
                'timeout': 10,
                'setup': self._setup_go
            },
            'php': {
                'extension': 'php',
                'command': 'php',
                'timeout': 10,
                'setup': None
            },
            'html': {
                'extension': 'html',
                'command': None,
                'timeout': 0,
                'setup': None
            },
            'css': {
                'extension': 'css',
                'command': None,
                'timeout': 0,
                'setup': None
            },
            'typescript': {
                'extension': 'ts',
                'command': None,
                'timeout': 10,
                'setup': self._setup_typescript
            }
        }
        
        # Create temp directory for code execution
        os.makedirs('temp_execution', exist_ok=True)
    
    def execute(self, code: str, language: str) -> Dict[str, Any]:
        """
        Execute code in the specified language
        
        Args:
            code: Source code to execute
            language: Programming language
            
        Returns:
            Dictionary with execution results
        """
        if language not in self.execution_configs:
            return {
                "success": False,
                "output": f"Unsupported language: {language}",
                "error": "Language not supported for execution"
            }
        
        # For HTML/CSS, just return the code as output
        if language in ['html', 'css']:
            return {
                "success": True,
                "output": code,
                "error": None,
                "execution_time": 0
            }
        
        # Create a temporary file for the code
        config = self.execution_configs[language]
        extension = config['extension']
        
        try:
            # Create a unique filename
            timestamp = int(time.time())
            filename = f"temp_execution/code_{timestamp}.{extension}"
            
            # Write code to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Run setup if needed
            command = config['command']
            if config['setup']:
                setup_result = config['setup'](filename)
                if not setup_result['success']:
                    return setup_result
                command = setup_result.get('command', command)
                filename = setup_result.get('filename', filename)
            
            # Execute the code
            start_time = time.time()
            result = self._run_command(command, filename, config['timeout'])
            execution_time = time.time() - start_time
            
            # Clean up temporary files
            self._cleanup(filename)
            
            return {
                "success": result['success'],
                "output": result['output'],
                "error": result['error'],
                "execution_time": round(execution_time, 3)
            }
            
        except Exception as e:
            logger.error(f"Error executing {language} code: {str(e)}")
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "execution_time": 0
            }
    
    def _run_command(self, command: str, filename: str, timeout: int) -> Dict[str, Any]:
        """
        Run a command with timeout
        
        Args:
            command: Command to run
            filename: File to execute
            timeout: Timeout in seconds
            
        Returns:
            Dictionary with command output
        """
        try:
            cmd = [command, filename]
            
            # Run the command with timeout
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            try:
                stdout, stderr = process.communicate(timeout=timeout)
                return {
                    "success": process.returncode == 0,
                    "output": stdout,
                    "error": stderr if process.returncode != 0 else None
                }
            except subprocess.TimeoutExpired:
                process.kill()
                return {
                    "success": False,
                    "output": "",
                    "error": f"Execution timed out after {timeout} seconds"
                }
                
        except Exception as e:
            logger.error(f"Error running command: {str(e)}")
            return {
                "success": False,
                "output": "",
                "error": str(e)
            }
    
    def _cleanup(self, filename: str) -> None:
        """
        Clean up temporary files
        
        Args:
            filename: File to remove
        """
        try:
            if os.path.exists(filename):
                os.remove(filename)
                
            # Remove any additional files created during compilation
            base_name = os.path.splitext(filename)[0]
            directory = os.path.dirname(filename)
            
            for file in os.listdir(directory):
                if file.startswith(os.path.basename(base_name)) and file != os.path.basename(filename):
                    os.remove(os.path.join(directory, file))
                    
        except Exception as e:
            logger.warning(f"Error cleaning up files: {str(e)}")
    
    def _setup_java(self, filename: str) -> Dict[str, Any]:
        """
        Setup for Java execution
        
        Args:
            filename: Java file to compile
            
        Returns:
            Dictionary with setup results
        """
        try:
            # Extract class name from file
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple regex to find public class name
            import re
            match = re.search(r'public\s+class\s+(\w+)', content)
            
            if not match:
                return {
                    "success": False,
                    "error": "Could not find public class name in Java code"
                }
            
            class_name = match.group(1)
            
            # Ensure the class name matches the filename
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Compile the Java file
            compile_cmd = ['javac', filename]
            compile_process = subprocess.Popen(
                compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            _, compile_stderr = compile_process.communicate()
            
            if compile_process.returncode != 0:
                return {
                    "success": False,
                    "error": f"Compilation error: {compile_stderr}"
                }
            
            # Return the command to run the compiled Java class
            directory = os.path.dirname(filename)
            return {
                "success": True,
                "command": "java",
                "filename": f"-cp {directory} {class_name}"
            }
            
        except Exception as e:
            logger.error(f"Error setting up Java execution: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _setup_cpp(self, filename: str) -> Dict[str, Any]:
        """
        Setup for C++ execution
        
        Args:
            filename: C++ file to compile
            
        Returns:
            Dictionary with setup results
        """
        try:
            # Get output executable name
            output_file = os.path.splitext(filename)[0]
            if os.name == 'nt':  # Windows
                output_file += '.exe'
            
            # Compile the C++ file
            compile_cmd = ['g++', filename, '-o', output_file]
            compile_process = subprocess.Popen(
                compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            _, compile_stderr = compile_process.communicate()
            
            if compile_process.returncode != 0:
                return {
                    "success": False,
                    "error": f"Compilation error: {compile_stderr}"
                }
            
            # Return the command to run the compiled executable
            return {
                "success": True,
                "command": output_file if os.name == 'nt' else f"./{os.path.basename(output_file)}",
                "filename": ""
            }
            
        except Exception as e:
            logger.error(f"Error setting up C++ execution: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _setup_csharp(self, filename: str) -> Dict[str, Any]:
        """
        Setup for C# execution
        
        Args:
            filename: C# file to compile
            
        Returns:
            Dictionary with setup results
        """
        try:
            # Create a temporary project
            directory = os.path.dirname(filename)
            project_name = f"temp_project_{int(time.time())}"
            project_dir = os.path.join(directory, project_name)
            
            os.makedirs(project_dir, exist_ok=True)
            
            # Create a new C# project
            create_cmd = ['dotnet', 'new', 'console', '-o', project_dir]
            create_process = subprocess.Popen(
                create_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            create_process.communicate()
            
            if create_process.returncode != 0:
                return {
                    "success": False,
                    "error": "Failed to create C# project"
                }
            
            # Copy the code to Program.cs
            with open(filename, 'r', encoding='utf-8') as f:
                code = f.read()
                
            with open(os.path.join(project_dir, 'Program.cs'), 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Return the command to run the C# project
            return {
                "success": True,
                "command": "dotnet",
                "filename": f"run --project {project_dir}"
            }
            
        except Exception as e:
            logger.error(f"Error setting up C# execution: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _setup_go(self, filename: str) -> Dict[str, Any]:
        """
        Setup for Go execution
        
        Args:
            filename: Go file to run
            
        Returns:
            Dictionary with setup results
        """
        # For Go, we can just use 'go run' directly
        return {
            "success": True,
            "command": "go",
            "filename": f"run {filename}"
        }
    
    def _setup_typescript(self, filename: str) -> Dict[str, Any]:
        """
        Setup for TypeScript execution
        
        Args:
            filename: TypeScript file to compile
            
        Returns:
            Dictionary with setup results
        """
        try:
            # Get output JavaScript file name
            js_file = os.path.splitext(filename)[0] + '.js'
            
            # Compile the TypeScript file
            compile_cmd = ['tsc', filename]
            compile_process = subprocess.Popen(
                compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            _, compile_stderr = compile_process.communicate()
            
            if compile_process.returncode != 0:
                return {
                    "success": False,
                    "error": f"Compilation error: {compile_stderr}"
                }
            
            # Return the command to run the compiled JavaScript
            return {
                "success": True,
                "command": "node",
                "filename": js_file
            }
            
        except Exception as e:
            logger.error(f"Error setting up TypeScript execution: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
