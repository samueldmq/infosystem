import json
import uuid
import unittest
import testtools

from infosystem.tests.functional import test_base


class DomainTestCase(test_base.CRUDTest,
                     testtools.TestCase):

    def load_fixtures(self):
        pass

    @property
    def resource_name(self):
        return 'domain'

    @property
    def required_attributes(self):
        return ['name']

    @property
    def optional_attributes(self):
        return ['active', 'parent_id']

    @property
    def unique_attributes(self):
        return [('name',)]

    def new_resource_ref(self):
        return {'name': uuid.uuid4().hex, 'active': True, 'parent_id': None}


if __name__ == '__main__':
    unittest.main()
