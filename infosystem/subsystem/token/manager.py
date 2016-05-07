import uuid

from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation


class Create(operation.Operation):

    def pre(self, data, **kwargs):
        username = data.get('name', None)
        password = data.get('password', None)

        users = self.manager.api.user.list(name=username, password=password)
        if not users:
            return False

        self.user = users[0]

        return self.user.is_stable()

    def do(self, session, **kwargs):
        token = self.driver.instantiate(id=uuid.uuid4().hex, user_id=self.user.id)

        self.driver.create(token, session=session)
        return token


class Manager(manager.Manager):

    def register_operations(self):
        self.create = Create(self)
        self.get = operation.Get(self)
        self.delete = operation.Delete(self)
