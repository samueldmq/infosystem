import flask

from infosystem.common.subsystem.controller import *
from infosystem.common.subsystem.driver import *
from infosystem.common.subsystem.manager import *
from infosystem.common.subsystem.router import *


class Subsystem(flask.Blueprint):

    def __init__(self, resource, router=None, controller=None, manager=None,
                 driver=None, operations=[]):
        super().__init__(resource.collection(), resource.collection())

        driver = driver(resource) if driver else Driver(resource)
        manager = manager(driver) if manager else Manager(driver)
        controller = controller(manager, resource.individual(), resource.collection()) if controller else Controller(manager, resource.individual(), resource.collection())
        router = router(controller, resource.collection(), routes=operations) if router else Router(controller, resource.collection(), routes=operations)

        self.name = resource.collection()
        self.router = router
        self.manager = manager
        self.register_routes()


    def register_routes(self):
        for route in self.router.routes:
            self.add_url_rule(
                route['url'], view_func=route['callback'], methods=[route['method']])
