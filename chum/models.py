from werkzeug.security import generate_password_hash

from chum import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    bucket_lists = db.relationship('BucketList', backref='user',
                                   lazy='dynamic',
                                   cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class BucketList(db.Model):
    __tablename__ = 'bucket_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    date_created = db.Column(db.String(50), nullable=False, unique=True)
    date_modified = db.Column(db.String(50), nullable=False, unique=True)
    items = db.relationship('BucketListItem', backref='bucket_list',
                            lazy='dynamic', cascade="all, delete-orphan")
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'),
                        nullable=False)


class BucketListItem(db.Model):
    __tablename__ = 'bucket_lists_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    done = db.Column(db.Boolean, default=False)
    bucket_list_id = db.Column(db.Integer, db.ForeignKey('BucketList.id'),
                               nullable=False)

