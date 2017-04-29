import json
import uuid
import unittest
import testtools

from infosystem.tests.functional import test_base


class PolicyTestCase(test_base.CRUDTest): #, testtools.TestCase):

    def load_fixtures(self):
        domain = self.post(
            resource_ref={'name': uuid.uuid4().hex, 'active': True},
            resource_name='domain',
            collection_name='domains')

        self.domain_id = domain['id']

    @property
    def resource_name(self):
        return 'policy'

    @property
    def required_attributes(self):
        return ['domain_id', 'name', 'url', 'method']

    @property
    def unique_attributes(self):
        return [('domain_id', 'name', 'url', 'method')]

    def new_resource_ref(self):
        return {'domain_id': self.domain_id,
                'name': uuid.uuid4().hex,
                'url': '/test',
                'method': 'GET'}


if __name__ == '__main__':
    unittest.main()
