from configparser import SafeConfigParser

# FIXME(fdoliveira) Check if read Unix style and than read windows
config_parser = SafeConfigParser()
config = config_parser.read('/etc/infosystem/infosystem.conf')
if config == []:
    config = config_parser.read('c:/etc/infosystem/infosystem.conf')


class Section(object):

    def __init__(self, name):
        self.name = name

    def __getattr__(self, name):
        return config_parser.get(self.name, name)


class Config(object):
    
    def __getattr__(self, name):
        return Section(name)


cfg = Config()
