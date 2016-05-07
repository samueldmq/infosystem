from infosystem.common.subsystem import driver
from infosystem.common.subsystem import operation


class Manager(object):

    def __init__(self, entity_cls):
        self.driver = driver.Driver(entity_cls)
        self.register_operations()

    def register_operations(self):
        self.create = operation.Create(self)
        self.get = operation.Get(self)
        self.list = operation.List(self)
        self.update = operation.Update(self)
        self.delete = operation.Delete(self)
