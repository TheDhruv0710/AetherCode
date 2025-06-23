from flask import Blueprint, jsonify, request, render_template
from services import analyze_repository, process_dialogue, generate_reports

main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/api/analyze_repo', methods=['POST'])
def analyze_repo():
    data = request.get_json()
    repo_url = data.get('repo_url')
    if not repo_url:
        return jsonify({'error': 'Repository URL is required'}), 400

    # This will call the placeholder function in services.py
    tech_spec = analyze_repository(repo_url)
    return jsonify(tech_spec)

@main_routes.route('/api/dialogue_turn', methods=['POST'])
def dialogue_turn():
    data = request.get_json()
    user_response = data.get('user_response')
    project_id = data.get('project_id')

    if not user_response or not project_id:
        return jsonify({'error': 'User response and project ID are required'}), 400

    # This will call the placeholder function in services.py
    ai_response = process_dialogue(project_id, user_response)
    return jsonify(ai_response)

@main_routes.route('/api/get_reports', methods=['GET'])
def get_reports():
    project_id = request.args.get('project_id')
    if not project_id:
        return jsonify({'error': 'Project ID is required'}), 400

    # This will call the placeholder function in services.py
    reports = generate_reports(project_id)
    return jsonify(reports)
