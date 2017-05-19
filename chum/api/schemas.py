from marshmallow import Schema, fields, validate


class UserRegisterSchema(Schema):
    name = fields.String(load_only=True, validate=[validate.Length(max=64)])
    username = fields.String(
        required=True,
        load_only=True,
        error_messages={
            'required': 'A username is required to register'}
    )
    email = fields.Email(required=True, load_only=True,
                         validate=[validate.Length(max=64)],
                         error_messages={
                             'required': 'An email is required to register'}
                         )
    password = fields.String(
        required=True,
        load_only=True,
        validate=[validate.Length(min=6)],
        error_messages={'required': 'Please send a password'}
    )
    password_again = fields.String(
        required=True,
        load_only=True,
        error_messages={'required': 'Please send the password again'})


class UserLoginSchema(Schema):
    username = fields.String(load_only=True)
    email = fields.Email(load_only=True, validate=[validate.Length(max=64)])
    password = fields.String(
        required=True,
        load_only=True,
        validate=[validate.Length(min=6)],
        error_messages={'required': 'Please send a password'}
    )


class BucketListItemSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True,
                         error_messages={
                             'required': 'Please send an item name'}
                         )
    description = fields.String()
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    done = fields.Boolean()
    url = fields.Method('get_url', dump_only=True)

    class Meta:
        ordered = True

    @staticmethod
    def get_url(obj):
        return obj.get_url()


class BucketListItemEditSchema(Schema):
    name = fields.String(load_only=True, required=True,
                         error_messages={
                             'required': 'Please send an item name'}
                         )
    description = fields.String(load_only=True, allow_none=True)
    done = fields.Boolean(load_only=True, allow_none=True)


class BucketListSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True,
                         error_messages={
                             'required': 'Please send a bucketlist name'}
                         )
    items = fields.Nested(BucketListItemSchema, dump_only=True, many=True)
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    created_by = fields.String(attribute='user.username', dump_only=True)
    url = fields.Method('get_url', dump_only=True)

    class Meta:
        ordered = True

    @staticmethod
    def get_url(obj):
        return obj.get_url()


get_bucketlists_schema = BucketListSchema(many=True)
single_bucketlist_schema = BucketListSchema()
bucketlist_item_schema = BucketListItemSchema()
edit_bucketlist_item_schema = BucketListItemEditSchema()
login_schema = UserLoginSchema()
register_schema = UserRegisterSchema()

