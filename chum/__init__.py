from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import app_configuration
from .models import db
from .api.resources import (
    UserAPI,
    BucketListsAPI,
    BucketListAPI,
    BucketListAddItemAPI,
    BucketListEditItemAPI
)


def create_app(config_name):
    # set default configuration settings
    default_config_name = 'production'
    if config_name is None:
        config_name = default_config_name

    # initialize Flask instance
    app = Flask(__name__, instance_relative_config=False, static_folder=None)

    # fetch configuration settings
    try:
        app.config.from_object(app_configuration[config_name])
    except KeyError as e:
        print("\n\t Invalid configuration key: '{}'. Defaulting...\n".format(
            e.args[0]))
        app.config.from_object(app_configuration[default_config_name])
    app.config.from_pyfile('config.py')

    # initialize the application for use with SQLAlchemy
    db.init_app(app)

    # initialize flask-migrate with the flask cli
    migrate = Migrate(app, db)

    api = Api(app)

    # create API endpoints
    api.add_resource(UserAPI, '/api/v1/auth/<string:arg>',
                     endpoint='user_login_and_register')

    api.add_resource(BucketListsAPI, '/api/v1/bucketlists',
                     '/api/v1/bucketlists/',
                     endpoint='fetch_or_add_bucketlists')

    api.add_resource(BucketListAPI, '/api/v1/bucketlists/<int:id>',
                     endpoint='single_bucketlist')

    api.add_resource(BucketListAddItemAPI,
                     '/api/v1/bucketlists/<int:id>/items',
                     '/api/v1/bucketlists/<int:id>/items/',
                     endpoint='add_bucketlist_item')

    api.add_resource(BucketListEditItemAPI,
                     '/api/v1/bucketlists/<int:bucket_list_id>/items/<int:id>',
                     endpoint='edit_bucketlist_item')

    return app
