import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # General configuration options
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_OAUTH2_TOKEN_URL = os.getenv('GOOGLE_OAUTH2_TOKEN_URL')

    # Database configuration
    DB_HOST = 'localhost'
    DB_PORT = '5432'
    DB_NAME = 'your_db_name'
    DB_USER = 'your_db_user'
    DB_PASSWORD = 'your_db_password'

class ProductionConfig(Config):
    # Production-specific configuration options
    DB_HOST = os.getenv('PRODUCTION_DB_HOST', 'production_db_host')
    DB_NAME = os.getenv('PRODUCTION_DB_NAME', 'production_db_name')
    DB_USER = os.getenv('PRODUCTION_DB_USER', 'production_db_user')
    DB_PASSWORD = os.getenv('PRODUCTION_DB_PASSWORD', 'production_db_password')

class DevelopmentConfig(Config):
    # Development-specific configuration options
    DB_HOST = os.getenv('DEVELOPMENT_DB_HOST', 'development_db_host')
    DB_NAME = os.getenv('DEVELOPMENT_DB_NAME', 'development_db_name')
    DB_USER = os.getenv('DEVELOPMENT_DB_USER', 'development_db_user')
    DB_PASSWORD = os.getenv('DEVELOPMENT_DB_PASSWORD', 'development_db_password')

def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig
    else:
        return DevelopmentConfig