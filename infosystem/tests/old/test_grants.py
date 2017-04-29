import json
import uuid
import unittest
import testtools

from infosystem.tests.functional import test_base


class GrantTestCase(test_base.CreateTest,
                    test_base.RetrieveTest,
                    test_base.DeleteTest,
                    testtools.TestCase):

    def load_fixtures(self):
        domain = self.post(
            resource_ref={'name': uuid.uuid4().hex, 'active': True},
            resource_name='domain',
            collection_name='domains')



        self.domain_id = domain['id']

    @property
    def resource_name(self):
        return 'grant'

    @property
    def required_attributes(self):
        return ['user_id', 'role_id']

    @property
    def unique_attributes(self):
        return [('user_id', 'role_id')]

    def new_resource_ref(self):
        user = self.post(
            resource_ref={'name': uuid.uuid4().hex,
                          'domain_id': self.domain_id,
                          'email': uuid.uuid4().hex,
                          'password': uuid.uuid4().hex,
                          'active': True},
            resource_name='user',
            collection_name='users')

        role = self.post(
            resource_ref={'name': uuid.uuid4().hex,
                          'domain_id': self.domain_id,
                          'active': True},
            resource_name='role',
            collection_name='roles')

        return {'user_id': user['id'],
                'role_id': role['id']}


if __name__ == '__main__':
    unittest.main()
