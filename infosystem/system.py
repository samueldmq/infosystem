from infosystem import database

import os

from infosystem import subsystem


class System(object):

    def __init__(self, additional_subsystems=[]):
        subsystem_list = subsystem.all + additional_subsystems
        controllers = [subsystem.Controller() for subsystem in subsystem_list]

        self.subsystems = {controller.manager.entity_name: controller
                           for controller in controllers}

        self.inject_dependencies()

    def inject_dependencies(self):
        api = lambda: None
        for name, subsystem in self.subsystems.items():
            setattr(api, name, subsystem.manager)

        # Dependency injection
        for subsystem in self.subsystems.values():
            subsystem.manager.api = api
