from flask import Flask
from api.auth import auth_bp
from api.products import products_bp
from api.orders import orders_bp
from database import db

app = Flask(__name__)
app.config.from_object('config')
# db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/api/auth')