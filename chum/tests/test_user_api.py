import json

from . import BaseTestCase


class TestUserAPI(BaseTestCase):

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
