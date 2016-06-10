import os

from gabbi import driver

from infosystem import application
from infosystem.tests import fixtures


TESTS_DIR = 'gabbits'


def load_tests(loader, tests, pattern):
    test_dir = os.path.join(os.path.dirname(__file__), TESTS_DIR)
    return driver.build_tests(test_dir, loader,
                              intercept=application.load_app,
                              fixture_module=fixtures)
