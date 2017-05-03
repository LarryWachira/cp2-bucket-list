from marshmallow import Schema, fields


class UserSchema(Schema):
    name = fields.String()
    username = fields.String()
    email = fields.Email()


class BucketListItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    done = fields.Boolean(dump_only=True)
    uri = fields.Url(dump_only=True)

    class Meta:
        ordered = True


class BucketListSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    items = fields.Nested(BucketListItemSchema, dump_only=True, many=True)
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    created_by = fields.String(attribute='user.username', dump_only=True)
    uri = fields.Url(dump_only=True)

    class Meta:
        ordered = True


bucketlists_schema = BucketListSchema(exclude=('items',), many=True)
single_bucketlist_schema = BucketListSchema()
