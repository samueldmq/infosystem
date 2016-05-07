from infosystem import database

from infosystem.subsystem import grant
from infosystem.subsystem import role
from infosystem.subsystem import token
from infosystem.subsystem import user
from infosystem.subsystem import domain


controllers = [domain.Controller(),
               grant.Controller(),
               role.Controller(),
               token.Controller(),
               user.Controller()]


subsystems = {c.entity_cls.get_name(): c for c in controllers}


class API(object):
    """Class that represents system APIs."""
    pass


api = API()
for name, controller in subsystems.items():
    setattr(api, name, controller.manager)


# Dependency injection
for subsystem in subsystems.values():
    subsystem.manager.api = api
