from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Session(db.Model):
    __tablename__ = 'sessions'

    id = db.Column(db.String(100), primary_key=True)  # Unique project_id
    repo_url = db.Column(db.String(500), nullable=False)
    repo_local_path = db.Column(db.String(500), nullable=True)
    tech_spec = db.Column(db.Text, nullable=True)
    mom_content = db.Column(db.Text, nullable=True)
    insights_content = db.Column(db.Text, nullable=True)
    code_health_report = db.Column(db.Text, nullable=True)
    file_structure = db.Column(db.Text, nullable=True)  # JSON string of file structure
    status = db.Column(db.String(50), default='pending', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to Message model
    messages = db.relationship('Message', backref='session', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'repo_url': self.repo_url,
            'repo_local_path': self.repo_local_path,
            'tech_spec': self.tech_spec,
            'mom_content': self.mom_content,
            'insights_content': self.insights_content,
            'code_health_report': self.code_health_report,
            'file_structure': json.loads(self.file_structure) if self.file_structure else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Session {self.id}>'

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), db.ForeignKey('sessions.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    code_lines_to_highlight = db.Column(db.Text, default='[]')  # JSON string

    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'code_lines_to_highlight': json.loads(self.code_lines_to_highlight) if self.code_lines_to_highlight else []
        }

    def __repr__(self):
        return f'<Message {self.id} from {self.role}>'
