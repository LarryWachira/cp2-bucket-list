from flask import Flask
from flask_migrate import Migrate

from config import app_configuration
from .models import db


def create_app(config_name):
    default_config_name = 'production'
    app = Flask(__name__, instance_relative_config=True)

    try:
        app.config.from_object(app_configuration[config_name])
    except KeyError as e:
        print("\n\t Invalid configuration key: '{}'. Defaulting...\n".format(
            e.args[0]))
        app.config.from_object(app_configuration[default_config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)

    migrate = Migrate(app, db)
    from . import models

    from .api.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    from .api.api import auth_api_bp
    app.register_blueprint(auth_api_bp, url_prefix='/api/v1')

    return app
