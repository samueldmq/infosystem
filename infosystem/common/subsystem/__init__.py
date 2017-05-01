import flask

# TODO(samueldmq): follow pattern for importing, import until after .subsystem
from infosystem.common.subsystem.controller import Controller
from infosystem.common.subsystem.driver import Driver
from infosystem.common.subsystem.manager import Manager
from infosystem.common.subsystem.router import Router


class Subsystem(flask.Blueprint):

    def __init__(self, resource=None, router=None, controller=None,
                 manager=None, driver=None, individual_name=None,
                 collection_name=None, operations=[]):
        individual_name = individual_name or resource.individual()
        collection_name = collection_name or resource.collection()

        super().__init__(collection_name, collection_name)

        driver = (driver(resource) if driver
                  else Driver(resource) if resource else None)
        manager = manager(driver) if manager else Manager(driver)
        if controller:
            controller = controller(manager, individual_name, collection_name)
        else:
            controller = Controller(manager, individual_name, collection_name)
        if router:
            router = router(controller, collection_name, routes=operations)
        else:
            router = Router(controller, collection_name, routes=operations)

        self.name = collection_name
        self.router = router
        self.manager = manager
        self.register_routes()

    def register_routes(self):
        for route in self.router.routes:
            self.add_url_rule(route['url'],
                              view_func=route['callback'],
                              methods=[route['method']])
