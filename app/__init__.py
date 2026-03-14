from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.routes.auth import auth
    from app.routes.farmer import farmer
    from app.routes.seller import seller
    from app.routes.admin import admin
    from app.routes.reports import reports

    app.register_blueprint(auth)
    app.register_blueprint(farmer)
    app.register_blueprint(seller)
    app.register_blueprint(admin)
    app.register_blueprint(reports)

    return app