from gabbi import fixture

import json
import requests
import uuid
import app
import os


class InfoSystemFixture(fixture.GabbiFixture):

    def __init__(self):
        super(InfoSystemFixture, self).__init__()

        self.client = app.app.test_client()


class UserFixture(InfoSystemFixture):
    """Fixture for tests involving users.

    This fixture creates 3 users and store the ID of one in 'user_id' envvar.

    """

    def start_fixture(self):
        headers={'Content-Type': 'application/json'}

        self.user_ids = []
        for i in range(3):
            data = {'name': uuid.uuid4().hex,
                    'email': uuid.uuid4().hex,
                    'active': True,
                    'password': uuid.uuid4().hex}
            response = self.client.post('/users',
                                        data=json.dumps(data),
                                        headers=headers)
            user = json.loads(response.data.decode())
            self.user_ids.append(user['user']['id'])

        os.environ['user_id'] = self.user_ids[0]

    def stop_fixture(self):
        for user_id in self.user_ids:
            self.client.delete('/users/' + user_id)
