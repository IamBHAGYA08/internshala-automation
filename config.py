import os

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SESSION_COOKIE_NAME = 'internshala_session'

    # SQLAlchemy (MySQL) configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://username:password@localhost/internshala_automation'

    # MongoDB configuration (optional)
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/internshala_automation'

    # Email settings (for notifications, alerts, etc.)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your-email@example.com'

    # Flask-Login settings
    LOGIN_MANAGER_LOGIN_VIEW = 'login'

    # Machine Learning configuration for internship recommendations
    MODEL_PATH = os.environ.get('MODEL_PATH') or './models/your_ml_model.pkl'

    # Monitoring and alerting system settings
    MONITORING_ENABLED = os.environ.get('MONITORING_ENABLED') or False
    ALERT_EMAIL = os.environ.get('ALERT_EMAIL') or 'admin@example.com'

    # Auto-apply assistant and resume parsing settings
    AUTO_APPLY_ENABLED = os.environ.get('AUTO_APPLY_ENABLED') or True
    RESUME_PARSING_ENABLED = os.environ.get('RESUME_PARSING_ENABLED') or True


# Development configuration class
class DevelopmentConfig(Config):
    DEBUG = True
    ENV = 'development'


# Production configuration class
class ProductionConfig(Config):
    DEBUG = False
    ENV = 'production'


# Testing configuration class
class TestingConfig(Config):
    TESTING = True
    ENV = 'testing'
