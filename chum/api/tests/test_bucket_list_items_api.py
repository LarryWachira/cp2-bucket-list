import json

from . import BaseTestCase


class TestBucketListItemsApi(BaseTestCase):

    def test_create_bucket_list_item(self):
        """ Test creating a bucketlist item """

        response = self.client.post('/api/v1/bucketlists/1/items/',
                                    data=json.dumps({'name': 'test',
                                                     'description': 'trial'}),
                                    headers={
                                        "Authorization": self.user_token},
                                    content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_edit_bucket_list_item(self):
        """ Test editing a bucketlist item """

        response = self.client.put('/api/v1/bucketlists/1/items/1',
                                   data=json.dumps({'name': 'test_trial'}),
                                   headers={
                                        "Authorization": self.user_token},
                                   content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_delete_bucket_list_item(self):
        """ Test deleting a bucketlist item """

        response = self.client.delete('/api/v1/bucketlists/1/items/1',
                                      headers={
                                       "Authorization": self.user_token})
        self.assertEqual(response.status_code, 204)
