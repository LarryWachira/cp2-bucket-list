import unittest

from chum import create_app, db
from chum.models import User, BucketList, BucketListItem


class BaseTestCase(unittest.TestCase):
    """
    Base test class for all tests
    """

    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.app_context()
        self.context.push()
        db.drop_all()
        db.create_all()
        self.client = self.app.test_client()

        self.user = User(
            name='Larry',
            username='larry',
            email='larry@example.org'
        )
        self.user.set_password('password')

        self.user2 = User(
            name='Larry Wachira',
            username='larry2',
            email='larry2@example.org'
        )
        self.user2.set_password('password')

        self.user3 = User(
            name='Larry Wachira Muchiri',
            username='larry3',
            email='larry3@example.org'
        )
        self.user3.set_password('password')

        self.user_token = self.user.generate_auth_token()
        self.user2_token = self.user.generate_auth_token()
        self.user3_token = self.user.generate_auth_token()

        self.user_bucket_list = BucketList(
            name='travel',
            user=self.user
        )

        self.user_bucket_list2 = BucketList(
            name='fun activities',
            user=self.user
        )

        self.user2_bucket_list = BucketList(
            name='food',
            user=self.user2
        )

        self.user3_bucket_list = BucketList(
            name='travel',
            user=self.user3
        )

        self.user_bucket_list_item = BucketListItem(
            name='Mombasa',
            bucket_list=self.user_bucket_list
        )

        self.user_bucket_list_item2 = BucketListItem(
            name='Mara',
            description='See a lot of lions!',
            bucket_list=self.user_bucket_list
        )

        self.user2_bucket_list_item = BucketListItem(
            name='Paris',
            bucket_list=self.user2_bucket_list
        )

        self.user3_bucket_list_item = BucketListItem(
            name='italy',
            description='Pasta.',
            bucket_list=self.user3_bucket_list
        )

        db.session.add_all([
            self.user,
            self.user2,
            self.user3,
            self.user_bucket_list,
            self.user_bucket_list2,
            self.user2_bucket_list,
            self.user3_bucket_list,
            self.user_bucket_list_item,
            self.user_bucket_list_item2,
            self.user2_bucket_list_item,
            self.user3_bucket_list_item
        ])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.context.pop()
