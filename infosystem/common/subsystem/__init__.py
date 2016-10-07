import flask

from infosystem.common.subsystem.controller import *
from infosystem.common.subsystem.driver import *
from infosystem.common.subsystem.manager import *
from infosystem.common.subsystem.router import *


class Subsystem(flask.Blueprint):

    def __init__(self, resource, router=None, controller=None, manager=None,
                 driver=None):
        super(Subsystem, self).__init__(resource.collection, resource.collection)

        if router is None:
            if controller is None:
                if manager is None:
                    if driver is None:
                        driver = Driver(resource)
                    manager = Manager(driver)
                controller = Contoller(manager)
            router = Router(controller)

        self.router = router
        self.register_routes()


    def register_routes(self):
        for route in self.router.routes:
            self.add_url_rule(
                route.url, view_func=route.callback, methods=[route.method])
