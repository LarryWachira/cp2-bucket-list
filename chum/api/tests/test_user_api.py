import json

from . import BaseTestCase


class TestUserAPI(BaseTestCase):

    def test_user_registration_and_login(self):
        """ Test that new user registration and log in is successful """

        # register new user
        user = {"username": "test",
                "email": "email@email.com",
                "password": "password",
                "password_again": "password"}
        response = self.client.post("/api/v1/auth/register",
                                    data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # log in created user
        response = self.client.post("/api/v1/auth/login",
                                    data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_invalid_login_details(self):
        """ Test that logging in with invalid credentials fails """

        # test with a user that does not exist
        user = {"username": "fail",
                "password": "password"}
        response = self.client.post("/api/v1/auth/login",
                                    data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 422)

        # test with user that exists but with invalid password
        user = {"username": "larry",
                "password": "passwad"}
        response = self.client.post("/api/v1/auth/login",
                                    data=json.dumps(user),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 422)
