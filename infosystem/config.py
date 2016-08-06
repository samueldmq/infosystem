import os

from configparser import SafeConfigParser


class Section(object):

    def __init__(self, name, parser):
        self.name = name
        self.parser = parser

    def __getattr__(self, name):
        return self.parser.get(self.name, name)


class Config(object):

    def __init__(self):
        self.parser = SafeConfigParser()
        # If the platform is Windows, add 'c:' as a prefix
        prefix = 'c:' if os.name == 'nt' else ''
        self.parser.read(prefix + '/etc/infosystem/infosystem.conf')

    def __getattr__(self, name):
        return Section(name, self.parser)


cfg = Config()
