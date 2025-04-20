from datetime import datetime
from .extensions import db  # Import db from extensions.py
from flask_login import UserMixin

# SQLAlchemy Models for MySQL
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    applications = db.relationship('Application', backref='user', lazy=True)  # Reverse relationship

    def __repr__(self):
        return f'<User {self.email}>'

class Internship(db.Model):
    __tablename__ = 'internships'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    skills = db.Column(db.String(200), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)  # Ensure this line exists
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Internship {self.title}>'

# MongoDB Models for storing ML-related or other non-relational data
class Application(db.Model):
    __tablename__ = 'applications'

   
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key for relationship

    def __repr__(self):
        return f'<Application {self.id} for {self.internship.title}>'

# New Alert Model
class Alert(db.Model):
    __tablename__ = 'alerts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    message = db.Column(db.String(256))
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='alerts')

    def __repr__(self):
        return f'<Alert {self.id} for {self.user.email}>'
