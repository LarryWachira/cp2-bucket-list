import json

from . import BaseTestCase


class TestBucketListApi(BaseTestCase):

    def test_fetch_all_bucket_lists(self):
        """ Test fetching all the bucketlist """

        response = self.client.get('/api/v1/bucketlists/', headers={
            "Authorization": self.user_token})
        self.assertEqual(response.status_code, 200)

    def test_that_get_all_bucket_lists_paginates(self):
        """ Test that get bucketlists response is paginated """

        response = self.client.get('/api/v1/bucketlists?limit=1', headers={
            "Authorization": self.user_token})
        self.assertTrue(response.data['page'] is not None)

    def test_create_bucket_list(self):
        """ Test creating a bucketlist """

        response = self.client.post('/api/v1/bucketlists/',
                                    data=json.dumps({'name': 'test'}),
                                    headers={
                                        "Authorization": self.user2_token},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_edit_bucket_list(self):
        """ Test editing a bucketlist """

        response = self.client.put('/api/v1/bucketlists/1',
                                   data=json.dumps({'name': 'test_trial'}),
                                   headers={
                                       "Authorization": self.user_token},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_fetch_single_bucket_list(self):
        """ Test fetching a single bucketlist """

        response = self.client.get('/api/v1/bucketlists/1',
                                   headers={
                                       "Authorization": self.user_token})
        self.assertEqual(response.status_code, 200)

    def test_delete_bucket_list(self):
        """ Test deleting a bucketlist """

        response = self.client.delete('/api/v1/bucketlists/1',
                                      headers={
                                          "Authorization": self.user_token})
        self.assertEqual(response.status_code, 204)
