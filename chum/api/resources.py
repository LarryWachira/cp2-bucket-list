from flask import g, request, jsonify
from flask_restful import Resource, abort

from .auth import auth_token
from .utils import error_response, success_response
from .schemas import (
    bucketlists_schema,
    single_bucketlist_schema,
    login_schema,
    register_schema
)
from ..models import (
    db,
    User,
    BucketList,
    BucketListItem
)


class UserAPI(Resource):
    def post(self, arg):
        # logging in
        if arg == 'login':

            # check that the request object has data
            if request.get_json():
                # validate and map request fields using schema
                result, errors = login_schema.load(request.get_json())

                # return validation errors if any
                if errors:
                    return error_response(validation_errors=errors)

                username = result.get('username')
                email = result.get('email')

                if not username and not email:
                    return error_response(message='Please send an email or '
                                                  'username to login')

                # get user from the db
                if username:
                    user = User.query.filter_by(
                        username=username.lower()).first()
                else:
                    user = User.query.filter_by(email=email.lower()).first()

                if not user:
                    return error_response(status=404, error='Not found',
                                          message='The user {} does not exist'
                                                  .format(username or email))

                # check password and return token if valid
                password = result.get('password')
                if user.verify_password(password):
                    token = user.generate_auth_token()
                    response = jsonify(
                        {'status': 200,
                         'message': 'Login successful',
                         'token': '{}'.format(token)}
                    )
                    response.status_code = 200
                    return response

                else:
                    return error_response(message='The password is incorrect')

            else:
                return error_response(message='No data was sent to the server')

        # registering
        elif arg == 'register':
            # check that the request contains data
            if request.get_json():
                # validate and map request fields using schema
                result, errors = register_schema.load(request.get_json())

                # return validation errors if any
                if errors:
                    return error_response(validation_errors=errors)

                # prepare values to be sent to the db
                name = result.get('name')  # returns none if name empty
                username = result['username'].lower()
                email = result['email'].lower()
                password = result['password']
                password_again = result['password_again']

                # check that no user with the same username or email exists
                user_by_username = User.query.filter_by(
                    username=username).first()
                user_by_email = User.query.filter_by(email=email).first()
                if user_by_username:
                    return error_response(status=422,
                                          error='Unprocessable entity',
                                          message='That username is already '
                                                  'taken')

                elif user_by_email:
                    return error_response(status=422,
                                          error='Unprocessable entity',
                                          message='That email already exists')

                # check that passwords match
                elif password != password_again:
                    return error_response(status=422,
                                          error='Unprocessable entity',
                                          message='Passwords do not match')

                # add new user to the database
                else:
                    user = User(name=name, username=username, email=email)
                    user.set_password(password)
                    db.session.add(user)
                    db.session.commit()

                    message = 'Thank you for registering, {}. ' \
                              'Your account has been successfully created. ' \
                              'Login to obtain an API authorization ' \
                              'token'.format(username)

                    return success_response(message=message, status=201)

            else:
                return error_response(status=400, error='Bad Request',
                                      message='No data was sent to the server')

        else:
            return error_response(status=404, error='Not found',
                                  message='Invalid url')


class BucketListsAPI(Resource):
    decorators = [auth_token.login_required]
    def get(self):
        bucketlists = BucketList.query.all()
        if not bucketlists:
            return success_response(message='No bucketlists have been added')
        result = bucketlists_schema.dump(list(bucketlists))
        return jsonify(result.data)

    def post(self):
        pass


class BucketListAPI(Resource):
    decorators = [auth_token.login_required]
    def get(self, id):
        bucketlist = BucketList.query.get(id)
        result = single_bucketlist_schema.dump(bucketlist)
        return jsonify(result.data)

    def put(self):
        pass

    def delete(self):
        pass


class BucketListItemsAPI(Resource):
    @auth_token.login_required
    def post(self):
        pass


class BucketListItemAPI(Resource):
    decorators = [auth_token.login_required]
    def put(self):
        pass

    def delete(self):
        pass
