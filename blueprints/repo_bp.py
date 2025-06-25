import os
import uuid
import json
import logging
from flask import Blueprint, request, jsonify
from models import db, Session
from services.repo_service import RepositoryService

logger = logging.getLogger(__name__)

repo_bp = Blueprint('repo', __name__)
repo_service = RepositoryService()

@repo_bp.route('/analyze', methods=['POST'])
def analyze_repository():
    """Analyze a GitHub repository"""
    try:
        from services.ai_service import AzureOpenAIService
        ai_service = AzureOpenAIService()
        
        data = request.get_json()
        repo_url = data.get('repo_url')
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        # Validate GitHub URL
        if not ('github.com' in repo_url or 'githubusercontent.com' in repo_url):
            return jsonify({'error': 'Only GitHub repositories are supported'}), 400
        
        # Generate unique project ID
        project_id = str(uuid.uuid4())
        
        # Clone repository
        logger.info(f"Starting analysis for repository: {repo_url}")
        repo_path = repo_service.clone_repository(repo_url, project_id)
        
        # Get repository info from GitHub API
        repo_info = repo_service.get_repository_info(repo_url)
        
        # Get file structure
        file_structure = repo_service.get_file_structure(repo_path)
        
        # Get key files for analysis
        key_files = repo_service.get_key_files(repo_path)
        
        # Get repository summary
        repo_summary = repo_service.get_repository_summary(repo_path)
        
        # Generate technical specification using AI
        tech_spec = ai_service.generate_tech_spec(repo_summary, key_files)
        
        # Create session in database
        session = Session(
            id=project_id,
            repo_url=repo_url,
            repo_local_path=repo_path,
            tech_spec=tech_spec,
            file_structure=json.dumps(file_structure),
            status='analyzed'
        )
        
        db.session.add(session)
        db.session.commit()
        
        logger.info(f"Repository analysis completed for project: {project_id}")
        
        return jsonify({
            'project_id': project_id,
            'repo_info': repo_info,
            'tech_spec': tech_spec,
            'files': file_structure,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error analyzing repository: {e}")
        return jsonify({
            'error': 'Failed to analyze repository',
            'details': str(e)
        }), 500

@repo_bp.route('/<project_id>/file', methods=['GET'])
def get_file_content(project_id):
    """Get content of a specific file"""
    try:
        file_path = request.args.get('path')
        
        if not file_path:
            return jsonify({'error': 'File path is required'}), 400
        
        # Get session from database
        session = Session.query.get(project_id)
        if not session:
            return jsonify({'error': 'Project not found'}), 404
        
        if not session.repo_local_path or not os.path.exists(session.repo_local_path):
            return jsonify({'error': 'Repository not found locally'}), 404
        
        # Get file content
        content = repo_service.get_file_content(session.repo_local_path, file_path)
        
        return jsonify({
            'content': content,
            'path': file_path,
            'status': 'success'
        })
        
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        logger.error(f"Error getting file content: {e}")
        return jsonify({
            'error': 'Failed to get file content',
            'details': str(e)
        }), 500

@repo_bp.route('/<project_id>/structure', methods=['GET'])
def get_repository_structure(project_id):
    """Get repository file structure"""
    try:
        # Get session from database
        session = Session.query.get(project_id)
        if not session:
            return jsonify({'error': 'Project not found'}), 404
        
        # Return cached file structure
        if session.file_structure:
            file_structure = json.loads(session.file_structure)
            return jsonify({
                'files': file_structure,
                'status': 'success'
            })
        
        # If not cached, regenerate
        if session.repo_local_path and os.path.exists(session.repo_local_path):
            file_structure = repo_service.get_file_structure(session.repo_local_path)
            
            # Update session with file structure
            session.file_structure = json.dumps(file_structure)
            db.session.commit()
            
            return jsonify({
                'files': file_structure,
                'status': 'success'
            })
        
        return jsonify({'error': 'Repository not found'}), 404
        
    except Exception as e:
        logger.error(f"Error getting repository structure: {e}")
        return jsonify({
            'error': 'Failed to get repository structure',
            'details': str(e)
        }), 500

@repo_bp.route('/<project_id>/info', methods=['GET'])
def get_project_info(project_id):
    """Get project information"""
    try:
        session = Session.query.get(project_id)
        if not session:
            return jsonify({'error': 'Project not found'}), 404
        
        return jsonify(session.to_dict())
        
    except Exception as e:
        logger.error(f"Error getting project info: {e}")
        return jsonify({
            'error': 'Failed to get project info',
            'details': str(e)
        }), 500

@repo_bp.route('/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project and cleanup resources"""
    try:
        session = Session.query.get(project_id)
        if not session:
            return jsonify({'error': 'Project not found'}), 404
        
        # Cleanup repository files
        repo_service.cleanup_repository(project_id)
        
        # Delete from database
        db.session.delete(session)
        db.session.commit()
        
        return jsonify({
            'message': 'Project deleted successfully',
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error deleting project: {e}")
        return jsonify({
            'error': 'Failed to delete project',
            'details': str(e)
        }), 500
