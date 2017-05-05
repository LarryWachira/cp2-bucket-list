from flask import g, request, jsonify
from flask_restful import Resource

from .auth import auth_token
from .utils import error_response, success_response
from .schemas import (
    get_bucketlists_schema,
    single_bucketlist_schema,
    login_schema,
    register_schema,
    bucketlist_item_schema
)
from ..models import (
    db,
    User,
    BucketList,
    BucketListItem
)


class UserAPI(Resource):
    """ A resource class to manage registration and logging in over the API """

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
                    return error_response(message='The password is incorrect',
                                          status=422,
                                          error='Unprocessable entity')

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
    """ A resource class to handle requests for many bucketlists """
    decorators = [auth_token.login_required]

    def get(self):
        # get bucketlists belonging to current user
        current_user_id = g.user.id
        bucketlists = BucketList.query.filter_by(user_id=current_user_id).all()

        if not bucketlists:
            return success_response(message='No bucketlists have been added')

        result = get_bucketlists_schema.dump(list(bucketlists))
        return jsonify(result.data)

    def post(self):
        print('\n\n\n\n\nrequest:', request.get_json(), '\n\n\n\n\n')
        if request.get_json():
            result, errors = single_bucketlist_schema.load(request.get_json())

            if errors:
                return error_response(validation_errors=errors)

            # create bucketlist object
            bucketlist = BucketList(name=result['name'])
            current_user = g.user
            bucketlist.user = current_user

            # add new bucketlist to the db
            db.session.add(bucketlist)
            db.session.commit()

            return success_response(message="Bucketlist successfully created",
                                    status=201,
                                    added=single_bucketlist_schema.dump(
                                        bucketlist).data
                                    )

        else:
            return error_response(status=400, error='Bad Request',
                                  message='No data was sent to the server')


class BucketListAPI(Resource):
    """ A resource class to handle requests for a single bucketlist """
    decorators = [auth_token.login_required]

    def get_bucketlist_object(self, id):
        # fetch bucketlists belonging to user
        current_user_id = g.user.id

        # fetch specified bucketlist
        bucketlist = BucketList.query.filter_by(
            user_id=current_user_id).filter_by(id=id).first()

        if not bucketlist:
            return error_response(
                message="Bucketlist {} was not found".format(id),
                status=404, error='Not found'
            )

        return bucketlist

    def get(self, id):
        bucketlist = self.get_bucketlist_object(id)

        # return error response if not bucketlist object
        if not isinstance(bucketlist, BucketList):
            return bucketlist

        # serialize bucketlist and return the result
        result = single_bucketlist_schema.dump(bucketlist)
        return jsonify(result.data)

    def put(self, id):
        # check that the request contains data
        print('\n\n\n\n\nrequest:', request.get_json(), '\n\n\n\n\n')
        if request.get_json():
            result, errors = single_bucketlist_schema.load(request.get_json())

            if errors:
                return error_response(validation_errors=errors)

            bucketlist = self.get_bucketlist_object(id)

            # return error response if not bucketlist object
            if type(bucketlist) is not BucketList:
                return bucketlist

            # edit the bucketlist
            new_name = result['name']
            bucketlist.name = new_name

            db.session.add(bucketlist)
            db.session.commit()

            return success_response(message='Bucketlist successfully modified',
                                    modified=single_bucketlist_schema.dump(
                                     bucketlist).data
                                    )

        else:
            return error_response(status=400, error='Bad Request',
                                  message='No data was sent to the server')

    def delete(self, id):
        bucketlist = self.get_bucketlist_object(id)

        # delete specified bucketlist
        db.session.delete(bucketlist)
        db.session.commit()

        return success_response(message='Bucketlist successfully '
                                'deleted', status=204)


class BucketListItemsAPI(Resource):
    @auth_token.login_required
    def post(self, id):
        pass


class BucketListItemAPI(Resource):
    decorators = [auth_token.login_required]

    def put(self, bucket_list_id, id):
        pass

    def delete(self, bucket_list_id, id):
        pass
