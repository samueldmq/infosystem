from gabbi import fixture

import json
import requests
import uuid
import app
import os


class InfoSystemFixture(fixture.GabbiFixture):
    """Create an entity and expose it via '<entity>_id' envvar."""

    def __init__(self):
        super(InfoSystemFixture, self).__init__()

        self.client = app.app.test_client()

    @property
    def entity_name(self):
        return NotImplemented

    @property
    def collection_name(self):
        return self.entity_name + 's'

    def new_entity(self):
        return NotImplemented

    def start_fixture(self):
        headers={'Content-Type': 'application/json'}
        self.data = self.new_entity()

        response = self.client.post('/' + self.collection_name,
                                    data=json.dumps(self.data),
                                    headers=headers)

        self.entity = json.loads(response.data.decode())[self.entity_name]
        os.environ[self.entity_name + '_id'] = self.entity['id']

    def stop_fixture(self):
        self.client.delete('/' + self.collection_name + '/' +
                           self.entity['id'])


class DomainFixture(InfoSystemFixture):

    @property
    def entity_name(self):
        return 'domain'

    def new_entity(self):
        return {'name': uuid.uuid4().hex,
                'active': True}


class UserFixture(InfoSystemFixture):

    @property
    def entity_name(self):
        return 'domain'

    def new_entity(self):
        return {'name': uuid.uuid4().hex,
                'email': uuid.uuid4().hex,
                'active': True,
                'password': uuid.uuid4().hex}


class TokenFixture(InfoSystemFixture):

    @property
    def entity_name(self):
        return 'token'

    def new_entity(self):
        return {'name': os.environ['user_id'],
                'password': uuid.uuid4().hex}
