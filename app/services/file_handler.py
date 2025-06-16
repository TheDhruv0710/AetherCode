"""
File handling service for AetherCode application
"""
import os
import tempfile
from app.services.code_analyzer import analyze_code, get_language_from_extension

def process_uploaded_files(files):
    """Process uploaded files for analysis"""
    if not files or files[0].filename == '':
        return {'error': 'No files selected'}
    
    try:
        results = []
        for file in files:
            # Save file temporarily
            temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(temp_dir, file.filename)
            file.save(file_path)
            
            # Determine language from file extension
            extension = os.path.splitext(file.filename)[1].lower()
            language = get_language_from_extension(extension)
            
            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    code = f.read()
            except UnicodeDecodeError:
                # Try with a different encoding if UTF-8 fails
                with open(file_path, 'r', encoding='latin-1') as f:
                    code = f.read()
            
            # Analyze code
            analysis = analyze_code(code, language)
            
            results.append({
                'filename': file.filename,
                'language': language,
                'analysis': analysis
            })
            
            # Clean up
            os.remove(file_path)
            os.rmdir(temp_dir)
        
        return {'results': results}
    except Exception as e:
        return {'error': str(e)}
