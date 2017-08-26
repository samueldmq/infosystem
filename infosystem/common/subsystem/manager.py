from infosystem.common.subsystem import operation


class Manager(object):

    def __init__(self, driver):
        self.driver = driver

        self.create = operation.Create(self)
        self.get = operation.Get(self)
        self.list = operation.List(self)
        self.update = operation.Update(self)
        self.delete = operation.Delete(self)
        # NOTE(samueldmq): what do we use this for ?
        self.count = operation.Count(self)
