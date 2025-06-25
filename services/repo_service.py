import os
import shutil
import tempfile
import logging
import zipfile
import io
from typing import Dict, List, Any, Optional
from pathlib import Path
import requests
import chardet
import pathspec
from github import Github
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class RepositoryService:
    def __init__(self, temp_dir: str = "temp_repos"):
        self.temp_dir = temp_dir
        os.makedirs(temp_dir, exist_ok=True)
        
    def _parse_github_url(self, repo_url: str) -> tuple[str, str]:
        """Parse GitHub URL to extract owner and repo name"""
        try:
            # Handle different GitHub URL formats
            if repo_url.endswith('.git'):
                repo_url = repo_url[:-4]
            
            # Parse URL
            parsed = urlparse(repo_url)
            path_parts = parsed.path.strip('/').split('/')
            
            if len(path_parts) >= 2:
                owner = path_parts[0]
                repo = path_parts[1]
                return owner, repo
            else:
                raise ValueError("Invalid GitHub URL format")
                
        except Exception as e:
            logger.error(f"Error parsing GitHub URL {repo_url}: {e}")
            raise Exception(f"Invalid GitHub URL format: {str(e)}")
    
    def clone_repository(self, repo_url: str, project_id: str) -> str:
        """Download a GitHub repository as ZIP and extract it"""
        try:
            owner, repo = self._parse_github_url(repo_url)
            repo_path = os.path.join(self.temp_dir, project_id)
            
            # Remove existing directory if it exists
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
            
            # Download repository as ZIP
            zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
            logger.info(f"Downloading repository {repo_url} as ZIP from {zip_url}")
            
            response = requests.get(zip_url, timeout=30)
            
            # If main branch doesn't exist, try master
            if response.status_code == 404:
                zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/master.zip"
                logger.info(f"Trying master branch: {zip_url}")
                response = requests.get(zip_url, timeout=30)
            
            if response.status_code != 200:
                raise Exception(f"Failed to download repository: HTTP {response.status_code}")
            
            # Extract ZIP file
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
                zip_file.extractall(self.temp_dir)
            
            # Find the extracted directory (it will have a name like repo-main or repo-master)
            extracted_dirs = [d for d in os.listdir(self.temp_dir) 
                            if d.startswith(f"{repo}-") and os.path.isdir(os.path.join(self.temp_dir, d))]
            
            if not extracted_dirs:
                raise Exception("Could not find extracted repository directory")
            
            # Rename to our project_id
            extracted_path = os.path.join(self.temp_dir, extracted_dirs[0])
            os.rename(extracted_path, repo_path)
            
            logger.info(f"Repository downloaded and extracted to {repo_path}")
            return repo_path
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error downloading repository: {e}")
            raise Exception(f"Failed to download repository: {str(e)}")
        except Exception as e:
            logger.error(f"Error downloading repository: {e}")
            raise Exception(f"Failed to download repository: {str(e)}")
    
    def get_file_structure(self, repo_path: str) -> List[Dict[str, Any]]:
        """Get the file structure of the repository"""
        try:
            # Load .gitignore patterns if exists
            gitignore_path = os.path.join(repo_path, '.gitignore')
            ignore_patterns = []
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r', encoding='utf-8', errors='ignore') as f:
                    ignore_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            # Add common patterns to ignore
            ignore_patterns.extend([
                '.git/**',
                '__pycache__/**',
                '*.pyc',
                'node_modules/**',
                '.env',
                '*.log',
                '.DS_Store',
                'Thumbs.db'
            ])
            
            spec = pathspec.PathSpec.from_lines('gitwildmatch', ignore_patterns)
            
            def build_tree(path: str, relative_path: str = "") -> List[Dict[str, Any]]:
                items = []
                try:
                    for item in sorted(os.listdir(path)):
                        item_path = os.path.join(path, item)
                        rel_path = os.path.join(relative_path, item).replace('\\', '/') if relative_path else item
                        
                        # Skip if matches gitignore patterns
                        if spec.match_file(rel_path):
                            continue
                            
                        if os.path.isdir(item_path):
                            # Directory
                            children = build_tree(item_path, rel_path)
                            items.append({
                                'name': item,
                                'path': rel_path,
                                'type': 'dir',
                                'children': children
                            })
                        else:
                            # File
                            items.append({
                                'name': item,
                                'path': rel_path,
                                'type': 'file',
                                'size': os.path.getsize(item_path)
                            })
                except PermissionError:
                    logger.warning(f"Permission denied accessing {path}")
                    
                return items
            
            return build_tree(repo_path)
            
        except Exception as e:
            logger.error(f"Error getting file structure: {e}")
            raise Exception(f"Failed to get file structure: {str(e)}")
    
    def get_file_content(self, repo_path: str, file_path: str) -> str:
        """Get content of a specific file"""
        try:
            full_path = os.path.join(repo_path, file_path)
            
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not os.path.isfile(full_path):
                raise Exception(f"Path is not a file: {file_path}")
            
            # Check file size (limit to 1MB)
            file_size = os.path.getsize(full_path)
            if file_size > 1024 * 1024:  # 1MB
                return f"// File too large to display ({file_size} bytes)\n// Please view this file in your local editor"
            
            # Detect encoding
            with open(full_path, 'rb') as f:
                raw_data = f.read()
                encoding_result = chardet.detect(raw_data)
                encoding = encoding_result['encoding'] or 'utf-8'
            
            # Read file content
            try:
                with open(full_path, 'r', encoding=encoding, errors='replace') as f:
                    content = f.read()
                return content
            except UnicodeDecodeError:
                # Fallback to binary representation for non-text files
                return f"// Binary file - cannot display content\n// File type: {os.path.splitext(file_path)[1]}"
                
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise Exception(f"Failed to read file: {str(e)}")
    
    def get_key_files(self, repo_path: str, max_files: int = 10) -> Dict[str, str]:
        """Get content of key files for analysis"""
        try:
            key_files = {}
            important_files = [
                'README.md', 'README.txt', 'README.rst',
                'package.json', 'requirements.txt', 'Pipfile', 'pyproject.toml',
                'Dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
                'main.py', 'app.py', 'index.js', 'server.js', 'main.js',
                'config.py', 'settings.py', 'config.js',
                '.env.example', 'environment.yml'
            ]
            
            # Look for important files first
            for file_name in important_files:
                file_path = os.path.join(repo_path, file_name)
                if os.path.exists(file_path) and os.path.isfile(file_path):
                    try:
                        content = self.get_file_content(repo_path, file_name)
                        key_files[file_name] = content
                        if len(key_files) >= max_files:
                            break
                    except Exception as e:
                        logger.warning(f"Could not read {file_name}: {e}")
            
            # If we need more files, look for source files
            if len(key_files) < max_files:
                source_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c', '.go', '.rs', '.php']
                
                for root, dirs, files in os.walk(repo_path):
                    # Skip hidden directories and common ignore patterns
                    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
                    
                    for file in files:
                        if len(key_files) >= max_files:
                            break
                            
                        file_ext = os.path.splitext(file)[1].lower()
                        if file_ext in source_extensions:
                            rel_path = os.path.relpath(os.path.join(root, file), repo_path).replace('\\', '/')
                            if rel_path not in key_files:
                                try:
                                    content = self.get_file_content(repo_path, rel_path)
                                    key_files[rel_path] = content
                                except Exception as e:
                                    logger.warning(f"Could not read {rel_path}: {e}")
                    
                    if len(key_files) >= max_files:
                        break
            
            return key_files
            
        except Exception as e:
            logger.error(f"Error getting key files: {e}")
            raise Exception(f"Failed to get key files: {str(e)}")
    
    def get_repository_summary(self, repo_path: str) -> str:
        """Get a summary of the repository structure"""
        try:
            file_structure = self.get_file_structure(repo_path)
            
            def count_items(items: List[Dict[str, Any]]) -> Dict[str, int]:
                counts = {'files': 0, 'directories': 0}
                for item in items:
                    if item['type'] == 'file':
                        counts['files'] += 1
                    elif item['type'] == 'dir':
                        counts['directories'] += 1
                        sub_counts = count_items(item.get('children', []))
                        counts['files'] += sub_counts['files']
                        counts['directories'] += sub_counts['directories']
                return counts
            
            counts = count_items(file_structure)
            
            # Get file extensions
            extensions = {}
            for root, dirs, files in os.walk(repo_path):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext:
                        extensions[ext] = extensions.get(ext, 0) + 1
            
            # Create summary
            summary = f"""Repository Structure Summary:
- Total Files: {counts['files']}
- Total Directories: {counts['directories']}

File Types:
"""
            for ext, count in sorted(extensions.items(), key=lambda x: x[1], reverse=True)[:10]:
                summary += f"- {ext}: {count} files\n"
            
            return summary
            
        except Exception as e:
            logger.error(f"Error getting repository summary: {e}")
            return f"Error generating repository summary: {str(e)}"
    
    def get_repository_info(self, repo_url: str) -> Dict[str, Any]:
        """Get repository information using PyGithub (optional, for enhanced metadata)"""
        try:
            owner, repo = self._parse_github_url(repo_url)
            
            # Use PyGithub to get repository metadata (no token needed for public repos)
            g = Github()
            github_repo = g.get_repo(f"{owner}/{repo}")
            
            return {
                'name': github_repo.name,
                'full_name': github_repo.full_name,
                'description': github_repo.description,
                'language': github_repo.language,
                'stars': github_repo.stargazers_count,
                'forks': github_repo.forks_count,
                'open_issues': github_repo.open_issues_count,
                'created_at': github_repo.created_at.isoformat() if github_repo.created_at else None,
                'updated_at': github_repo.updated_at.isoformat() if github_repo.updated_at else None,
                'default_branch': github_repo.default_branch,
                'topics': github_repo.get_topics(),
                'license': github_repo.license.name if github_repo.license else None,
                'size': github_repo.size
            }
            
        except Exception as e:
            logger.warning(f"Could not get repository info from GitHub API: {e}")
            # Return basic info parsed from URL
            owner, repo = self._parse_github_url(repo_url)
            return {
                'name': repo,
                'full_name': f"{owner}/{repo}",
                'description': None,
                'language': None
            }
    
    def cleanup_repository(self, project_id: str):
        """Clean up downloaded repository"""
        try:
            repo_path = os.path.join(self.temp_dir, project_id)
            if os.path.exists(repo_path):
                shutil.rmtree(repo_path)
                logger.info(f"Cleaned up repository: {repo_path}")
        except Exception as e:
            logger.warning(f"Error cleaning up repository {project_id}: {e}")
