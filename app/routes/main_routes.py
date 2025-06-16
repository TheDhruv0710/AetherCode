"""
Main routes for AetherCode application
"""
from flask import Blueprint, render_template, current_app, send_from_directory, url_for
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html')

@main_bp.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory(os.path.join(current_app.root_path, '../static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
