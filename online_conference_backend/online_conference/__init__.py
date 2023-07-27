from flask import Flask
from config import Config
import psycopg2

def create_app():
    app = Flask(__name__)

    # Load configuration based on the environment
    config_class = get_config()
    app.config.from_object(config_class)

    # Iniitalize Flask extensions here


    # Initialize the database
    from . import db
    db.init_app(app)

    # Register blueprints here
    from online_conference.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app