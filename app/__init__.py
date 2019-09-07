from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail

from config import Config

db = SQLAlchemy()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
mail = Mail()

from app.auth.models import User
@login.user_loader
def load_user(uid):
    return User.query.get(uid)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bootstrap.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    from app.web import bp as web_bp
    app.register_blueprint(web_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.auth.controllers import auth as auth_module
    app.register_blueprint(auth_module)


    return app
