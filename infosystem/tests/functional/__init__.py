import os

from gabbi import driver

import infosystem
from infosystem.tests.functional import fixtures


def load_tests(loader, tests, pattern):
    test_dir = os.path.dirname(__file__)
    return driver.build_tests(test_dir, loader,
                              intercept=infosystem.System,
                              fixture_module=fixtures)
