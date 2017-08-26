import uuid
import sqlalchemy

# TODO this import here is so strange
from infosystem import database
from infosystem.common import exception


class Operation(object):

    def __init__(self, manager):
        self.manager = manager
        self.driver = manager.driver if hasattr(manager, 'driver') else None

    def pre(self, **kwargs):
        return True

    def do(self, **kwargs):
        return True

    def post(self):
        pass

    def __call__(self, **kwargs):
        session = kwargs.pop('session', database.db.session)

        if not self.pre(session=session, **kwargs):
            raise exception.PreconditionFailed()

        if not getattr(session, 'count', None):
            setattr(session, 'count', 1)
        else:
            session.count += 1

        try:
            result = self.do(session, **kwargs)
            session.count -= 1

            self.post()
            if session.count == 0:
                session.commit()
        except sqlalchemy.exc.IntegrityError:
            # TODO(samueldmq): integrity error may be something else...
            session.rollback()
            session.count = 0
            raise exception.DuplicatedEntity()
        except Exception as e:
            session.rollback()
            session.count = 0
            raise e
        return result


class Create(Operation):

    def pre(self, session, **kwargs):
        self.entity = self.driver.instantiate(id=uuid.uuid4().hex, **kwargs)
        return self.entity.is_stable()

    def do(self, session, **kwargs):
        self.driver.create(self.entity, session=session)
        return self.entity


class Get(Operation):

    def pre(self, session, id, **kwargs):
        self.id = id
        return True

    def do(self, session, **kwargs):
        entity = self.driver.get(self.id, session=session)
        return entity


class List(Operation):

    def do(self, session, **kwargs):
        entities = self.driver.list(session=session, **kwargs)
        return entities


class Update(Operation):

    def pre(self, session, id, **kwargs):
        self.id = id
        return True

    def do(self, session, **kwargs):
        entity = self.driver.update(self.id, kwargs, session=session)
        return entity


class Delete(Operation):

    def pre(self, session, id, **kwargs):
        self.entity = self.driver.get(id, session=session)
        return True

    def do(self, session, **kwargs):
        self.driver.delete(self.entity, session=session)


class Count(Operation):

    def do(self, session, **kwargs):
        rows = self.driver.count(session=session)
        return rows
