from datetime import datetime
from app import db
from flask_login import UserMixin

# SQLAlchemy Models for MySQL
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class Internship(db.Model):
    __tablename__ = 'internships'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Internship {self.title}>'

# MongoDB Models for storing ML-related or other non-relational data
class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internships.id'), nullable=False)
    status = db.Column(db.String(100), nullable=False, default="Applied")
    apply_date = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='applications')
    internship = db.relationship('Internship', backref='applications')

    def __repr__(self):
        return f'<Application {self.id} for {self.internship.title}>'
