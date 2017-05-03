from flask_restful import Api, Resource, fields, marshal_with, abort

from ..models import User, BucketList, BucketListItem


bucket_lists_fields = {
    'name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.String(attribute='user.username'),
    'uri': fields.Url('bucketlist', absolute=True)
}

bucket_list_items_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('bucketlist_item', absolute=True)
}


bucket_list_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'items': fields.List(fields.Nested(bucket_list_items_fields))
}


class UserAPI(Resource):
    def post(self, arg):
        pass


class BucketListsAPI(Resource):
    @marshal_with(bucket_lists_fields)
    def get(self):
        bucketlists = BucketList.query.all()
        return bucketlists

    def post(self):
        pass


class BucketListAPI(Resource):
    @marshal_with(bucket_list_fields)
    def get(self, id):
        bucketlist = BucketList.query.get(id)
        return bucketlist

    def put(self):
        pass

    def delete(self):
        pass


class BucketListItemsAPI(Resource):
    def post(self):
        pass


class BucketListItemAPI(Resource):
    def put(self):
        pass

    def delete(self):
        pass
