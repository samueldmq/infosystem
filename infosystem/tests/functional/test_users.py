import json
import uuid
import unittest
import testtools

from infosystem.tests.functional import test_base


class UserTestCase(test_base.CRUDTest,
                   testtools.TestCase):

    def load_fixtures(self):
        domain = self.post(
            resource_ref={'name': uuid.uuid4().hex, 'active': True},
            resource_name='domain',
            collection_name='domains')

        self.domain_id = domain['id']

    @property
    def resource_name(self):
        return 'user'

    @property
    def required_attributes(self):
        return ['name', 'domain_id', 'email', 'password']

    @property
    def optional_attributes(self):
        return ['active']

    @property
    def unique_attributes(self):
        return [('name', 'domain_id')]

    @property
    def hidden_attributes(self):
        return ['password']

    def new_resource_ref(self):
        return {'name': uuid.uuid4().hex,
                'domain_id': self.domain_id,
                'email': uuid.uuid4().hex,
                'password': uuid.uuid4().hex,
                'active': True}


if __name__ == '__main__':
    unittest.main()
