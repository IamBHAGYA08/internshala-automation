from flask import Flask
from .extensions import db
from .models import User, Internship, Application, Alert
from .routes import main_bp  # Import blueprint for routes
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    
    # Configurations (you can create a config file for this)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://bhagya:bhagyapassword@localhost/dbname'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    
    # Register blueprints
    app.register_blueprint(main_bp)  # Replace with the actual blueprint you're using
    
    return app
