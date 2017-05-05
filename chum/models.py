from datetime import datetime

from flask import current_app, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer,
    BadSignature,
    SignatureExpired
)


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=True)
    username = db.Column(db.String(50), nullable=False, index=True,
                         unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    bucket_lists = db.relationship('BucketList', backref='user',
                                   lazy='dynamic',
                                   cascade="all, delete-orphan")

    def __repr__(self):
        return '<User: {}>'.format(self.name)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600*24):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return 'Bearer ' + s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BadSignature:
            return "Invalid token"
        except SignatureExpired:
            return "Token expired"
        return User.query.get(data['id'])


class BucketList(db.Model):
    __tablename__ = 'bucket_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now, nullable=False)
    date_modified = db.Column(db.DateTime, default=datetime.now,
                              onupdate=datetime.now, nullable=False)
    items = db.relationship('BucketListItem', backref='bucket_list',
                            lazy='dynamic', cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<Bucket list: {}>'.format(self.name)

    def get_url(self):
        return url_for('single_bucketlist', id=self.id, _external=True)


class BucketListItem(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.Text, index=True, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.now)
    date_modified = db.Column(db.DateTime, default=datetime.now,
                              onupdate=datetime.now)
    done = db.Column(db.Boolean, default=False)
    bucket_list_id = db.Column(db.Integer, db.ForeignKey('bucket_lists.id'),
                               nullable=False)

    def __repr__(self):
        return '<Bucket list item: {}>'.format(self.name)

    def get_url(self):
        return url_for('edit_bucketlist_item', id=self.id,
                       bucket_list_id=self.bucket_list_id, _external=True)
