from infosystem.common.subsystem import driver
from infosystem.common.subsystem import operation


class Manager(object):

    def __init__(self, entity_cls=None):
        self.entity_cls = entity_cls
        self.driver = driver.Driver(entity_cls) if entity_cls else None
        self.register_operations()

    @property
    def entity_name(self):
        return self.entity_cls.get_name()

    @property
    def collection_name(self):
        return self.entity_cls.get_collection_name()

    def register_operations(self):
        if self.driver:
            self.create = operation.Create(self)
            self.get = operation.Get(self)
            self.list = operation.List(self)
            self.update = operation.Update(self)
            self.delete = operation.Delete(self)
            self.count = operation.Count(self)
