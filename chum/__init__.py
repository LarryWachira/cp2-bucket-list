from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import app_configuration
from .models import db
from .api.resources import (
    UserAPI,
    BucketListsAPI, BucketListAPI,
    BucketListItemsAPI, BucketListItemAPI
)


def create_app(config_name):
    default_config_name = 'production'

    if config_name is None:
        config_name = default_config_name

    app = Flask(__name__, instance_relative_config=True)

    # fetch configuration settings
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

    api = Api(app)

    # Create API endpoints
    api.add_resource(UserAPI, '/api/v1/auth/<string:arg>',
                     endpoint='user')

    api.add_resource(BucketListsAPI, '/api/v1/bucketlists',
                     '/api/v1/bucketlists/', endpoint='bucketlists')

    api.add_resource(BucketListAPI, '/api/v1/bucketlists/<int:id>',
                     endpoint='bucketlist')

    api.add_resource(BucketListItemsAPI,
                     '/api/v1/bucketlists/<int:id>/items',
                     '/api/v1/bucketlists/<int:id>/items/',
                     endpoint='bucketlist_add_item')

    api.add_resource(BucketListItemAPI,
                     '/api/v1/bucketlists/<int:bucket_list_id>/items/<int:id>',
                     endpoint='bucketlist_item')

    return app
