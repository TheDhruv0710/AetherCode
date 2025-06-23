"""
GitHub API module for AetherCode.
This module provides functions to interact with GitHub repositories using only Python libraries,
without requiring a local Git installation.
"""
import os
import json
import tempfile
import shutil
import time
import zipfile
import requests
from urllib.parse import urlparse
from io import BytesIO

def parse_repo_url(repo_url):
    """
    Parse a GitHub repository URL to extract owner and repo name.
    Supports HTTPS and SSH URL formats.
    
    Args:
        repo_url (str): GitHub repository URL
        
    Returns:
        tuple: (owner, repo_name)
    """
    if repo_url.startswith("git@"):
        # SSH URL format: git@github.com:owner/repo.git
        parts = repo_url.split(":")
        if len(parts) != 2:
            raise ValueError(f"Invalid SSH repository URL: {repo_url}")
        
        path = parts[1].replace(".git", "")
        owner, repo = path.split("/")
        return owner, repo
    else:
        # HTTP(S) URL format: https://github.com/owner/repo
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip("/").split("/")
        
        if len(path_parts) < 2:
            raise ValueError(f"Invalid repository URL: {repo_url}")
        
        owner = path_parts[0]
        repo = path_parts[1].replace(".git", "")
        return owner, repo

def download_repository(repo_url, branch="main"):
    """
    Download a GitHub repository as a ZIP file and extract it.
    
    Args:
        repo_url (str): GitHub repository URL
        branch (str): Branch to download (default: main)
        
    Returns:
        str: Path to the extracted repository directory
    """
    # Parse the repository URL
    owner, repo = parse_repo_url(repo_url)
    
    # Create a directory in the project folder instead of system temp
    # This avoids permission issues on systems where temp directory is not writable
    current_dir = os.path.dirname(os.path.abspath(__file__))
    temp_base = os.path.join(current_dir, "temp_repos")
    os.makedirs(temp_base, exist_ok=True)
    repo_dir = os.path.join(temp_base, f"aethercode_{repo}_{int(time.time())}")
    os.makedirs(repo_dir, exist_ok=True)
    
    # Download the repository ZIP file
    zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
    print(f"Downloading repository: {zip_url}")
    
    response = requests.get(zip_url, stream=True)
    response.raise_for_status()
    
    # Extract the ZIP file directly from memory
    print(f"Extracting repository to: {repo_dir}")
    with zipfile.ZipFile(BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(repo_dir)
    
    # The extracted directory will have a name like "repo-main"
    extracted_dirs = [d for d in os.listdir(repo_dir) if os.path.isdir(os.path.join(repo_dir, d))]
    if not extracted_dirs:
        raise ValueError("No directories found in the extracted repository")
    
    # Return the path to the extracted repository
    return os.path.join(repo_dir, extracted_dirs[0])

def get_repository_structure(repo_dir):
    """
    Get the structure of a repository directory.
    
    Args:
        repo_dir (str): Path to the repository directory
        
    Returns:
        str: String representation of the repository structure
    """
    structure = []
    max_files = 50  # Limit the number of files to avoid overwhelming the API
    file_count = 0
    
    for root, dirs, files in os.walk(repo_dir):
        if '.git' in root:
            continue
            
        level = root.replace(repo_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        folder_name = os.path.basename(root)
        
        if level == 0:
            structure.append(f"Repository structure:")
        else:
            structure.append(f"{indent}{folder_name}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        for file in files:
            if file_count >= max_files:
                structure.append(f"{sub_indent}... (more files)")
                break
            structure.append(f"{sub_indent}{file}")
            file_count += 1
    
    return '\n'.join(structure)

def get_key_file_contents(repo_dir):
    """
    Get the contents of key files in the repository.
    
    Args:
        repo_dir (str): Path to the repository directory
        
    Returns:
        str: String representation of key file contents
    """
    # Define key file patterns to look for
    key_files = [
        'README.md', 'README.txt', 'readme.md',
        'package.json', 'requirements.txt', 'setup.py',
        'Dockerfile', 'docker-compose.yml',
        '.gitignore', '.env.example'
    ]
    
    contents = []
    files_found = 0
    max_files = 5  # Limit the number of files to avoid overwhelming the API
    max_lines = 50  # Limit the number of lines per file
    
    # First look for exact matches
    for key_file in key_files:
        for root, _, files in os.walk(repo_dir):
            if files_found >= max_files:
                break
                
            if key_file in files:
                file_path = os.path.join(root, key_file)
                rel_path = os.path.relpath(file_path, repo_dir)
                
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()[:max_lines]
                        
                    contents.append(f"File: {rel_path}")
                    contents.append("-" * 40)
                    contents.append(''.join(lines))
                    contents.append("")
                    
                    files_found += 1
                    if files_found >= max_files:
                        break
                except Exception as e:
                    contents.append(f"Error reading {rel_path}: {e}")
    
    # If we haven't found enough files, look for other interesting files
    if files_found < max_files:
        interesting_extensions = ['.py', '.js', '.ts', '.java', '.c', '.cpp', '.h', '.cs', '.go', '.rs']
        
        for root, _, files in os.walk(repo_dir):
            if files_found >= max_files:
                break
                
            for file in files:
                if files_found >= max_files:
                    break
                    
                _, ext = os.path.splitext(file)
                if ext.lower() in interesting_extensions:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, repo_dir)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()[:max_lines]
                            
                        contents.append(f"File: {rel_path}")
                        contents.append("-" * 40)
                        contents.append(''.join(lines))
                        contents.append("")
                        
                        files_found += 1
                    except Exception as e:
                        pass  # Skip files that can't be read
    
    if not contents:
        return "No key files found or could not read file contents."
    
    return '\n'.join(contents)

def get_repository_info(repo_url):
    """
    Get information about a GitHub repository using the GitHub API.
    
    Args:
        repo_url (str): GitHub repository URL
        
    Returns:
        dict: Repository information
    """
    # Parse the repository URL
    owner, repo = parse_repo_url(repo_url)
    
    # Get repository information from GitHub API
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(api_url)
    response.raise_for_status()
    
    # Get repository data
    repo_data = response.json()
    
    # Get commit history
    commits_url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    commits_response = requests.get(commits_url, params={'per_page': 10})
    commits_response.raise_for_status()
    
    # Format commit history
    commit_history = []
    for commit in commits_response.json():
        commit_history.append(f"{commit['sha'][:7]} - {commit['commit']['message'].split(chr(10))[0]} ({commit['commit']['author']['name']})")
    
    return {
        'repository': repo_data,
        'commit_history': commit_history
    }

def analyze_github_repository(repo_url):
    """
    Analyze a GitHub repository without requiring a local Git installation.
    
    Args:
        repo_url (str): GitHub repository URL
        
    Returns:
        dict: Repository analysis results
    """
    try:
        # Get repository information from GitHub API
        repo_info = get_repository_info(repo_url)
        
        # Download the repository
        repo_dir = download_repository(repo_url)
        
        # Analyze the repository structure
        file_structure = get_repository_structure(repo_dir)
        
        # Get key file contents
        file_contents = get_key_file_contents(repo_dir)
        
        # Format commit history
        commit_history = '\n'.join(repo_info['commit_history'])
        
        # Clean up the downloaded repository
        shutil.rmtree(os.path.dirname(repo_dir))
        
        return {
            'repo_url': repo_url,
            'file_structure': file_structure,
            'file_contents': file_contents,
            'commit_history': commit_history,
            'repository_info': repo_info['repository']
        }
    except Exception as e:
        return {
            'error': str(e),
            'repo_url': repo_url
        }
