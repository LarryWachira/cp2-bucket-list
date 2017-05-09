from flask import g, request, jsonify, url_for
from flask_restful import Resource

from .auth import auth_token
from .utils import error_response, success_response
from .schemas import (
    get_bucketlists_schema,
    single_bucketlist_schema,
    login_schema,
    register_schema,
    bucketlist_item_schema,
    edit_bucketlist_item_schema
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
        # obtain pagination arguments from the URL's query string
        page = request.args.get('page', 1, type=int)
        max_limit = 100
        request_limit = request.args.get('limit', 20, type=int)
        limit = min(request_limit, max_limit)
        search_term = request.args.get('q', None, type=str)

        # get paginated bucketlists belonging to current user
        current_user_id = g.user.id

        # all bucketlists
        if not search_term:
            paginated_bucketlists = BucketList.query.filter_by(
                user_id=current_user_id).paginate(page, limit, error_out=True)

        # searched bucketlists if search url argument exists
        else:
            paginated_bucketlists = BucketList.query.filter_by(
                user_id=current_user_id).filter(BucketList.name.ilike(
                 '%' + search_term + '%')).paginate(page, limit,
                                                    error_out=True)

        # return 404 if the user doesn't have bucketlists
        if not paginated_bucketlists.items:
            return error_response(error='Not found', status=404,
                                  message='No bucketlists have been added')

        # obtain prev_url and next_url
        if paginated_bucketlists.has_prev:
            previous_url = url_for(request.endpoint,
                                   q=search_term, limit=limit,
                                   page=paginated_bucketlists.prev_num,
                                   _external=True)
        else:
            previous_url = None

        if paginated_bucketlists.has_next:
            next_url = url_for(request.endpoint,
                               q=search_term, limit=limit,
                               page=paginated_bucketlists.next_num,
                               _external=True)
        else:
            next_url = None

        # obtain first and last urls
        first_url = url_for(request.endpoint, q=search_term, limit=limit,
                            page=1, _external=True)
        last_url = url_for(request.endpoint, q=search_term,
                           limit=limit, page=paginated_bucketlists.pages,
                           _external=True)

        # serialize bucketlist objects
        result = get_bucketlists_schema.dump(list(paginated_bucketlists.items))

        return jsonify({
            'page': page,
            'limit': limit,
            'pages': paginated_bucketlists.pages,
            'prev_url': previous_url,
            'next_url': next_url,
            'first_url': first_url,
            'last_url': last_url,
            'total': paginated_bucketlists.total,
            'bucketlist(s)': result.data
        })

    def post(self):
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
        if request.get_json():
            result, errors = single_bucketlist_schema.load(request.get_json())

            if errors:
                return error_response(validation_errors=errors)

            bucketlist = self.get_bucketlist_object(id)

            # return error response if not bucketlist object
            if not isinstance(bucketlist, BucketList):
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

        # return error response if not bucketlist object
        if not isinstance(bucketlist, BucketList):
            return bucketlist

        # delete specified bucketlist
        db.session.delete(bucketlist)
        db.session.commit()

        return success_response(message='Bucketlist successfully '
                                'deleted', status=204)


class BucketListAddItemAPI(Resource):
    """ A resource class to handle requests for adding a bucketlist item """
    @auth_token.login_required
    def post(self, id):

        if request.get_json():
            bucket_list_id = id

            # validate request data
            result, errors = bucketlist_item_schema.load(
                request.get_json())

            # return validation errors if any
            if errors:
                return error_response(validation_errors=errors)

            # fetch bucket list
            bucketlist = BucketList.query.get(bucket_list_id)

            response = error_response(status=404, error='Not found',
                                      message='Bucketlist {} does not '
                                              'exist'.format(bucket_list_id))

            # verify that the bucketlist exists
            if not bucketlist:
                return response

            # verify bucketlist is owned by the current user
            elif bucketlist.user != g.user:
                return response

            else:
                name = result['name']
                description = result.get('description')
                done = result.get('done')

                # create bucketlist item object
                bucketlist_item = BucketListItem(name=name,
                                                 description=description,
                                                 done=done)

                # relate item to bucket list
                bucketlist_item.bucket_list = bucketlist

                # add bucket list item to db
                db.session.add(bucketlist_item)
                db.session.commit()

                return success_response(
                    message="Bucketlist item successfully created",
                    status=201,
                    added=bucketlist_item_schema.dump(
                        bucketlist_item).data
                    )

        else:
            return error_response(status=400, error='Bad Request',
                                  message='No data was sent to the server')


class BucketListEditItemAPI(Resource):
    """ A resource class to handle requests for editing a bucketlist item """
    decorators = [auth_token.login_required]

    def get_bucket_list_item_object(self, bucket_list_id, id):
        # fetch objects
        bucketlist = BucketList.query.get(bucket_list_id)
        bucketlist_item = BucketListItem.query.get(id)

        response_404 = error_response(status=404, error='Not found',
                                      message='Bucketlist {} does not '
                                      'exist'.format(bucket_list_id))

        # return 404 if bucket list owner is not current user
        if bucketlist.user != g.user:
            return response_404

        # return 404 if bucket list does not exist
        elif not bucketlist:
            return response_404

        # return 404 if bucket list item does not exist
        elif not bucketlist_item:
            return response_404

        # return item object
        else:
            return bucketlist_item

    def put(self, bucket_list_id, id):
        if request.get_json():
            bucketlist_item = self.get_bucket_list_item_object(
                bucket_list_id, id)

            # return 404 if not object
            if not isinstance(bucketlist_item, BucketListItem):
                return bucketlist_item

            # validate request data and modify item attributes accordingly
            result, errors = edit_bucketlist_item_schema.load(
                request.get_json())
            if errors:
                return error_response(validation_errors=errors)

            elif result.get('name') and not result.get('description'):
                bucketlist_item.name = result['name']
                bucketlist_item.done = result.get('done') or False

            elif not result.get('name') and result.get('description'):
                bucketlist_item.description = result['description']
                bucketlist_item.done = result.get('done') or False

            else:
                bucketlist_item.name = result['name']
                bucketlist_item.description = result['description']
                bucketlist_item.done = result.get('done') or False

            # add modified bucket list item to db
            db.session.add(bucketlist_item)
            db.session.commit()

            return success_response(
                message="Bucketlist item successfully modified",
                modified=bucketlist_item_schema.dump(
                    bucketlist_item).data
            )

        else:
            return error_response(status=400, error='Bad Request',
                                  message='No data was sent to the server')

    def delete(self, bucket_list_id, id):
        bucketlist_item = self.get_bucket_list_item_object(bucket_list_id, id)

        # return error response if not bucketlist object
        if not isinstance(bucketlist_item, BucketListItem):
            return bucketlist_item

        # delete specified bucketlist
        db.session.delete(bucketlist_item)
        db.session.commit()

        return success_response(message='Bucketlist item successfully '
                                        'deleted', status=204)
