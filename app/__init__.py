from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo
from flask_mail import Mail
from flask_login import LoginManager
from config import Config

# Initialize extensions
db = SQLAlchemy()
mongo = PyMongo()
mail = Mail()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    mongo.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

