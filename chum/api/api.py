from flask import Blueprint
from flask_restful import Api, Resource


api_bp = Blueprint('api', __name__)
auth_api_bp = Blueprint('auth', __name__)

api = Api(api_bp)
auth = Api(auth_api_bp)


class UserAPI(Resource):
    pass


class BucketListAPI(Resource):
    pass


class BucketListItemsAPI(Resource):
    pass

