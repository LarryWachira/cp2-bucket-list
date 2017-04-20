import json

from . import BaseTestCase


class TestAPI(BaseTestCase):

    def test_user_registration_and_login(self):
        """ Test that new user registration and log in is successful """

        # register new user
        user = {"username": "test",
                "password": "password"}
        response = self.client.post("/api/v1/auth/register",
                                    data=json.dumps(user))
        self.assertEqual(response.status_code, 201)

        # log in created user
        response = self.client.post("/api/v1/auth/login",
                                    data=json.dumps(user))
        self.assertEqual(response.status_code, 200)

    def test_invalid_login_details(self):
        """ Test that logging in with invalid credentials fails """

        user = {"username": "fail",
                "password": "password"}
        response = self.client.post("/api/v1/auth/login",
                                    data=json.dumps(user))
        self.assertEqual(response.status_code, 403)

    def test_fetch_all_bucket_lists(self):
        response = self.client.get('/api/v1/bucketlists/', headers={
                                        "Authorization": self.user_token})
        self.assertTrue(response.status_code == 200)

    def test_create_bucket_list(self):
        response = self.client.post('/api/v1/bucketlists/',
                                    data=json.dumps({'name': 'test'}),
                                    headers={
                                        "Authorization": self.user_token})
        self.assertTrue(response.status_code == 201)

    def test_edit_bucket_list(self):
        response = self.client.put('/api/v1/bucketlists/5',
                                   data=json.dumps({'name': 'test_trial'}),
                                   headers={
                                        "Authorization": self.user_token})
        self.assertTrue(response.status_code == 201)

    def test_fetch_single_bucket_list(self):
        response = self.client.get('/api/v1/bucketlists/5', headers={
            "Authorization": self.user_token})
        self.assertTrue(response.status_code == 200)

    def test_delete_bucket_list(self):
        response = self.client.delete('/api/v1/bucketlists/5',
                                      headers={
                                       "Authorization": self.user_token})
        self.assertTrue(response.status_code == 204)

    def test_create_bucket_list_item(self):
        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    data=json.dumps({'name': 'test',
                                                     'description': 'trial'}),
                                    headers={
                                        "Authorization": self.user_token})
        self.assertTrue(response.status_code == 201)

    def test_edit_bucket_list_item(self):
        response = self.client.put('/api/v1/bucketlists/1/items/6',
                                   data=json.dumps({'name': 'test_trial'}),
                                   headers={
                                        "Authorization": self.user_token})
        self.assertTrue(response.status_code == 201)

    def test_delete_bucket_list_item(self):
        response = self.client.delete('/api/v1/bucketlists/1/items/6',
                                      headers={
                                       "Authorization": self.user_token})
        self.assertTrue(response.status_code == 204)
