from flask import Flask

from config import config
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_moment import Moment
from flask_mail import Mail
from flask_pagedown import PageDown

DEBUG = True

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
mail = Mail()
pagedown = PageDown()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'admin.login'


def create_app(config_name):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    # 附加路由和自定义的错误页面
    from app.main import main as main_blueprint
    from app.admin import admin as admin_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    return app
