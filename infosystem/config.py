from configparser import SafeConfigParser


config_parser = SafeConfigParser()
config_parser.read('/etc/infosystem/infosystem.conf')


class Section(object):

    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        return config_parser.get(self.name, name)


class Config(object):
    
    def __getattr__(self, name):
        return Section(name)


cfg = Config()
