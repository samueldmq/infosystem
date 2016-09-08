import uuid

from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation


class Create(operation.Operation):

    def pre(self, data, **kwargs):
        # FIXME(samueldmq): this method needs to receive the parameters
        # explicitly.
        if kwargs.get('user'):
            # FIXME(samueldmq): how to avoid someone simply passing the user
            # in the body and then having a valid token?
            self.user = kwargs['user']
        else:
            domain_name = data.get('domain_name', None)
            username = data.get('username', None)
            password = data.get('password', None)

            # TODO(samueldmq): allow get by unique attrs
            domains = self.manager.api.domain.list(name=domain_name)

            if not domains:
                return False

            domain_id = domains[0].id

            users = self.manager.api.user.list(domain_id=domain_id, name=username, password=password)
            if not users:
                return False

            self.user = users[0]

        return self.user.is_stable()

    def do(self, session, **kwargs):
        # TODO(samueldmq): use self.user.id instead of self.user_id
        token = self.driver.instantiate(id=uuid.uuid4().hex, user_id=self.user.id)

        self.driver.create(token, session=session)
        return token


class Manager(manager.Manager):

    def register_operations(self):
        self.create = Create(self)
        self.get = operation.Get(self)
        self.delete = operation.Delete(self)
