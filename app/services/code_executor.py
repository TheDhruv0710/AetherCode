"""
Code execution service for AetherCode application
"""
import subprocess
import tempfile
import os
import time
from app.config.language_config import LANGUAGE_CONFIGS

def run_code(code, language):
    """Execute code in the specified language and return the output"""
    config = LANGUAGE_CONFIGS.get(language)
    if not config:
        return {'error': f'Unsupported language: {language}'}
    
    # Create temporary directory and file
    temp_dir = tempfile.mkdtemp()
    file_path = os.path.join(temp_dir, f"main{config['extension']}")
    
    try:
        # Write code to temporary file
        with open(file_path, 'w') as f:
            f.write(code)
        
        output = ""
        error = ""
        
        # Handle compiled languages
        if 'compile_command' in config:
            compile_cmd = f"{config['compile_command']} {file_path}"
            compile_process = subprocess.run(
                compile_cmd,
                shell=True,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=config['timeout']
            )
            
            if compile_process.returncode != 0:
                return {'error': compile_process.stderr}
        
        # Execute code
        if language == 'java':
            # Special handling for Java
            execute_cmd = f"{config['command']} {config['main_class']}"
        elif language == 'csharp':
            # Special handling for C#
            execute_cmd = config['command']
        elif language == 'go':
            # Special handling for Go
            execute_cmd = f"{config['command']} {file_path}"
        else:
            execute_cmd = f"{config['command']} {file_path}"
        
        start_time = time.time()
        process = subprocess.run(
            execute_cmd,
            shell=True,
            cwd=temp_dir,
            capture_output=True,
            text=True,
            timeout=config['timeout']
        )
        execution_time = time.time() - start_time
        
        output = process.stdout
        error = process.stderr
        
        if process.returncode != 0 and error:
            return {'error': error}
        
        return {
            'output': output,
            'execution_time': f"{execution_time:.2f}s"
        }
    
    except subprocess.TimeoutExpired:
        return {'error': f'Execution timed out after {config["timeout"]} seconds'}
    except Exception as e:
        return {'error': str(e)}
    finally:
        # Clean up temporary files
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
