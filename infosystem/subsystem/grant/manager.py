from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation


class Manager(manager.Manager):

    def register_operations(self):
        self.create = operation.Create(self)
        self.get = operation.Get(self)
        self.list = operation.List(self)
        self.delete = operation.Delete(self)
