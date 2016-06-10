import os
import json
import requests
import uuid


from gabbi import fixture

from infosystem import application


entities = {}


def add_entity(collection, entity):
    """Store an entity in the list of elements of its collection."""
    if collection not in entities:
        entities[collection] =  []

    entities[collection].append(entity)


def get_attr(collection, attr):
    """Get value of attr in first entity of the collection."""
    return entities.get(collection, {})[0][attr]


class InfoSystemFixture(fixture.GabbiFixture):
    """Create an entity and expose it via '<entity>_id' envvar."""

    def __init__(self):
        super(InfoSystemFixture, self).__init__()

        self.client = application.load_app().test_client()

        # Request and store an admin token to perform the fixture creation
        response = self.client.post(
            '/tokens',
            data=json.dumps({'name': 'admin', 'password': '123456'}),
            headers={'Content-Type': 'application/json'})

        self.admin_token = json.loads(response.data.decode())['token']['id']

    @property
    def entity_name(self):
        return NotImplemented

    @property
    def collection_name(self):
        return self.entity_name + 's'

    def new_entity(self):
        return NotImplemented

    def start_fixture(self):
        headers={'Content-Type': 'application/json',
                 'token': self.admin_token}
        self.data = self.new_entity()

        response = self.client.post('/' + self.collection_name,
                                    data=json.dumps(self.data),
                                    headers=headers)

        self.entity = json.loads(response.data.decode())[self.entity_name]

        # Adds information not returned by the server, such as user's password
        self.entity.update(self.data)

        add_entity(self.collection_name, self.entity)
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
        return 'user'

    def new_entity(self):
        return {'domain_id': get_attr('domains', 'id'),
                'name': uuid.uuid4().hex,
                'email': uuid.uuid4().hex,
                'active': True,
                'password': uuid.uuid4().hex}


class TokenFixture(InfoSystemFixture):

    @property
    def entity_name(self):
        return 'token'

    def new_entity(self):
        return {'name': get_attr('users', 'id'),
                'password': get_attr('users', 'password')}
