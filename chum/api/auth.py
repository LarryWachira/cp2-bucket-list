from flask import g
from flask_httpauth import HTTPTokenAuth

from .utils import error_response
from ..models import User


auth_token = HTTPTokenAuth("Bearer")


@auth_token.verify_token
def verify_auth_token(token):
    g.user = User.verify_auth_token(token)
    return g.user not in ['Invalid token', 'Token expired']


@auth_token.error_handler
def unauthorized_token():
    return error_response(status=401, error='Unauthorized',
                          message='Please send a valid authentication token')
