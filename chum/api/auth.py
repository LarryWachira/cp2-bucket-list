from flask import current_app, g, jsonify
from flask_httpauth import HTTPTokenAuth

from ..models import User


auth_token = HTTPTokenAuth("Bearer")


@auth_token.verify_token
def verify_auth_token(token):
    if current_app.config.get('IGNORE_AUTH') is True:
        g.user = User.query.get(1)
    else:
        g.user = User.verify_auth_token(token)
    return g.user is not None


@auth_token.error_handler
def unauthorized_token():
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please send your authentication token'})
    response.status_code = 401
    return response
