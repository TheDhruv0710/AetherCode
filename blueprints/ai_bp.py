import json
import logging
from flask import Blueprint, request, jsonify, send_file
from models import db, Session, Message
from services.repo_service import RepositoryService

logger = logging.getLogger(__name__)

ai_bp = Blueprint('ai', __name__)
repo_service = RepositoryService()

@ai_bp.route('/chat', methods=['POST'])
def chat_with_ai():
    """Chat with AI about the repository"""
    try:
        from services.ai_service import AzureOpenAIService
        ai_service = AzureOpenAIService()
        
        data = request.get_json()
        project_id = data.get('project_id')
        user_message = data.get('message')
        
        if not project_id or not user_message:
            return jsonify({'error': 'Project ID and message are required'}), 400
        
        # Get session from database
        session = Session.query.get(project_id)
        if not session:
            return jsonify({'error': 'Project not found'}), 404
        
        # Save user message
        user_msg = Message(
            session_id=project_id,
            role='user',
            content=user_message
        )
        db.session.add(user_msg)
        
        # Get conversation history
        messages = Message.query.filter_by(session_id=project_id).order_by(Message.timestamp).all()
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Add current user message to conversation
        conversation_history.append({"role": "user", "content": user_message})
        
        # Prepare repository context
        repo_context = ""
        if session.tech_spec:
            repo_context += f"Technical Specification:\n{session.tech_spec}\n\n"
        
        if session.repo_local_path:
            try:
                repo_summary = repo_service.get_repository_summary(session.repo_local_path)
                repo_context += f"Repository Summary:\n{repo_summary}\n\n"
            except Exception as e:
                logger.warning(f"Could not get repository summary: {e}")
        
        # Get AI response with session-based state tracking
        ai_response_data = ai_service.chat(user_message, session_id=project_id)
        
        ai_response = ai_response_data.get('response', 'I apologize, but I encountered an error processing your request.')
        mom_update = ai_response_data.get('mom_update', '')
        insights_update = ai_response_data.get('insights_update', '')
        
        # Save AI message
        ai_msg = Message(
            session_id=project_id,
            role='assistant',
            content=ai_response
        )
        db.session.add(ai_msg)
        
        # Update session with meeting minutes and insights
        if mom_update:
            current_mom = session.mom_content or ""
            session.mom_content = f"{current_mom}\n- {mom_update}".strip()
        
        if insights_update:
            current_insights = session.insights_content or ""
            session.insights_content = f"{current_insights}\n- {insights_update}".strip()
        
        db.session.commit()
        
        return jsonify({
            'response': ai_response,
            'mom': session.mom_content,
            'insights': session.insights_content,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error in AI chat: {e}")
        return jsonify({
            'error': 'Failed to process chat message',
            'details': str(e)
        }), 500

@ai_bp.route('/reports/<project_id>', methods=['GET'])
def generate_reports(project_id):
    """Generate comprehensive reports for the project"""
    try:
        from services.ai_service import AzureOpenAIService
        ai_service = AzureOpenAIService()
        
        # Get session from database
        session = Session.query.get(project_id)
        if not session:
            return jsonify({'error': 'Project not found'}), 404
        
        # Get conversation history
        messages = Message.query.filter_by(session_id=project_id).order_by(Message.timestamp).all()
        conversation_history = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Prepare repository context
        repo_summary = ""
        key_files = {}
        
        if session.repo_local_path:
            try:
                repo_summary = repo_service.get_repository_summary(session.repo_local_path)
                key_files = repo_service.get_key_files(session.repo_local_path, max_files=5)
            except Exception as e:
                logger.warning(f"Could not get repository data for reports: {e}")
        
        # Generate reports using AI
        reports = {}
        
        # Generate code health report
        try:
            code_health_report = ai_service.generate_code_health_report(
                repo_summary, key_files, conversation_history
            )
            reports['code_health_report'] = code_health_report
            session.code_health_report = code_health_report
        except Exception as e:
            logger.error(f"Error generating code health report: {e}")
            reports['code_health_report'] = f"Error generating code health report: {str(e)}"
        
        # Generate meeting minutes
        try:
            if conversation_history:
                mom_report = ai_service.generate_meeting_minutes(conversation_history)
                reports['mom_content'] = mom_report
                session.mom_content = mom_report
            else:
                reports['mom_content'] = "No conversation history available for meeting minutes."
        except Exception as e:
            logger.error(f"Error generating meeting minutes: {e}")
            reports['mom_content'] = f"Error generating meeting minutes: {str(e)}"
        
        # Generate insights report
        try:
            if conversation_history:
                insights_report = ai_service.generate_insights_report(conversation_history, repo_summary)
                reports['insights_content'] = insights_report
                session.insights_content = insights_report
            else:
                reports['insights_content'] = "No conversation history available for insights."
        except Exception as e:
            logger.error(f"Error generating insights report: {e}")
            reports['insights_content'] = f"Error generating insights report: {str(e)}"
        
        # Update session status
        session.status = 'completed'
        db.session.commit()
        
        return jsonify({
            **reports,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error generating reports: {e}")
        return jsonify({
            'error': 'Failed to generate reports',
            'details': str(e)
        }), 500

@ai_bp.route('/conversation/<project_id>', methods=['GET'])
def get_conversation_history(project_id):
    """Get conversation history for a project"""
    try:
        # Get session from database
        session = Session.query.get(project_id)
        if not session:
            return jsonify({'error': 'Project not found'}), 404
        
        # Get messages
        messages = Message.query.filter_by(session_id=project_id).order_by(Message.timestamp).all()
        
        return jsonify({
            'messages': [msg.to_dict() for msg in messages],
            'mom_content': session.mom_content,
            'insights_content': session.insights_content,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        return jsonify({
            'error': 'Failed to get conversation history',
            'details': str(e)
        }), 500

@ai_bp.route('/regenerate-tech-spec/<project_id>', methods=['POST'])
def regenerate_tech_spec(project_id):
    """Regenerate technical specification for a project"""
    try:
        from services.ai_service import AzureOpenAIService
        ai_service = AzureOpenAIService()
        
        # Get session from database
        session = Session.query.get(project_id)
        if not session:
            return jsonify({'error': 'Project not found'}), 404
        
        if not session.repo_local_path:
            return jsonify({'error': 'Repository not found locally'}), 404
        
        # Get repository data
        repo_summary = repo_service.get_repository_summary(session.repo_local_path)
        key_files = repo_service.get_key_files(session.repo_local_path)
        
        # Generate new technical specification
        tech_spec = ai_service.generate_tech_spec(repo_summary, key_files, session_id=project_id)
        
        # Update session
        session.tech_spec = tech_spec
        db.session.commit()
        
        return jsonify({
            'tech_spec': tech_spec,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error regenerating tech spec: {e}")
        return jsonify({
            'error': 'Failed to regenerate technical specification',
            'details': str(e)
        }), 500

@ai_bp.route('/status', methods=['GET'])
def ai_status():
    """Get AI service status and configuration info"""
    try:
        from services.ai_service import AzureOpenAIService
        import os
        
        ai_service = AzureOpenAIService()
        
        # Get environment variable status (without exposing sensitive data)
        env_status = {
            'api_key_configured': bool(os.getenv('AZURE_OPENAI_API_KEY') and 
                                     os.getenv('AZURE_OPENAI_API_KEY') not in ['your_api_key_here', 'your-api-key-here', '']),
            'endpoint_configured': bool(os.getenv('AZURE_OPENAI_ENDPOINT') and 
                                      os.getenv('AZURE_OPENAI_ENDPOINT') not in ['https://your-resource.openai.azure.com/', 'https://your-resource-name.openai.azure.com/', '']),
            'deployment_configured': bool(os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME') and 
                                        os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME') not in ['gpt-4', 'your-deployment-name', '']),
            'api_version': os.getenv('AZURE_OPENAI_API_VERSION', '2024-02-15-preview'),
            'endpoint_preview': os.getenv('AZURE_OPENAI_ENDPOINT', 'Not set')[:50] + '...' if os.getenv('AZURE_OPENAI_ENDPOINT') else 'Not set',
            'deployment_name': os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME', 'Not set')
        }
        
        return jsonify({
            'test_mode': ai_service.test_mode,
            'client_initialized': ai_service.client is not None,
            'environment_variables': env_status,
            'status': 'AI service ready' if not ai_service.test_mode else 'Running in test mode'
        })
        
    except Exception as e:
        logger.error(f"Error checking AI status: {e}")
        return jsonify({
            'error': 'Failed to check AI status',
            'details': str(e)
        }), 500

@ai_bp.route('/reports/<int:session_id>/download/<report_type>', methods=['GET'])
def download_report(session_id, report_type):
    """Generate and download report files"""
    try:
        from services.ai_service import AzureOpenAIService
        from services.repo_service import RepositoryService
        from flask import send_file
        import tempfile
        import os
        from datetime import datetime
        
        # Validate report type
        valid_types = ['tech_spec', 'code_health', 'meeting_minutes', 'insights']
        if report_type not in valid_types:
            return jsonify({'error': 'Invalid report type'}), 400
        
        # Get session
        session = Session.query.get(session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Initialize services
        ai_service = AzureOpenAIService()
        repo_service = RepositoryService()
        
        # Get repository info
        repo_info = repo_service.get_repository_info(session.repo_path)
        file_contents = repo_service.get_key_files_content(session.repo_path)
        
        # Generate report content based on type
        if report_type == 'tech_spec':
            content = ai_service.generate_tech_spec(repo_info.get('structure', ''), file_contents, session_id=session_id)
            filename = f"Technical_Specification_{session.repo_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        elif report_type == 'code_health':
            content = ai_service.generate_code_health_report(repo_info.get('structure', ''), file_contents, session_id=session_id)
            filename = f"Code_Health_Report_{session.repo_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        elif report_type == 'meeting_minutes':
            # Get conversation history
            messages = Message.query.filter_by(session_id=session_id).order_by(Message.timestamp).all()
            conversation = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
            content = ai_service.generate_meeting_minutes(conversation, repo_info.get('structure', ''), session_id=session_id)
            filename = f"Meeting_Minutes_{session.repo_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        elif report_type == 'insights':
            # Get conversation history
            messages = Message.query.filter_by(session_id=session_id).order_by(Message.timestamp).all()
            conversation = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
            content = ai_service.generate_insights_report(conversation, repo_info.get('structure', ''), file_contents, session_id=session_id)
            filename = f"Project_Insights_{session.repo_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # Create temporary file
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Return file for download
        return send_file(
            file_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/markdown'
        )
        
    except Exception as e:
        logger.error(f"Error generating report download: {e}")
        return jsonify({
            'error': 'Failed to generate report file',
            'details': str(e)
        }), 500

@ai_bp.route('/reports/<int:session_id>/export', methods=['GET'])
def export_all_reports(session_id):
    """Generate and download all reports as a ZIP file"""
    try:
        from services.ai_service import AzureOpenAIService
        from services.repo_service import RepositoryService
        from flask import send_file
        import tempfile
        import os
        import zipfile
        from datetime import datetime
        
        # Get session
        session = Session.query.get(session_id)
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Initialize services
        ai_service = AzureOpenAIService()
        repo_service = RepositoryService()
        
        # Get repository info
        repo_info = repo_service.get_repository_info(session.repo_path)
        file_contents = repo_service.get_key_files_content(session.repo_path)
        
        # Get conversation history
        messages = Message.query.filter_by(session_id=session_id).order_by(Message.timestamp).all()
        conversation = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
        
        # Generate all reports
        reports = {
            'Technical_Specification.md': ai_service.generate_tech_spec(repo_info.get('structure', ''), file_contents, session_id=session_id),
            'Code_Health_Report.md': ai_service.generate_code_health_report(repo_info.get('structure', ''), file_contents, session_id=session_id),
            'Meeting_Minutes.md': ai_service.generate_meeting_minutes(conversation, repo_info.get('structure', ''), session_id=session_id),
            'Project_Insights.md': ai_service.generate_insights_report(conversation, repo_info.get('structure', ''), file_contents, session_id=session_id)
        }
        
        # Create temporary directory and ZIP file
        temp_dir = tempfile.mkdtemp()
        zip_filename = f"AetherCode_Reports_{session.repo_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        zip_path = os.path.join(temp_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename, content in reports.items():
                zipf.writestr(filename, content)
        
        # Return ZIP file for download
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        
    except Exception as e:
        logger.error(f"Error generating reports export: {e}")
        return jsonify({
            'error': 'Failed to generate reports export',
            'details': str(e)
        }), 500
