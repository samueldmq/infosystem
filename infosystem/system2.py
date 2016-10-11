from infosystem import database

import os

from infosystem import subsystem2
from infosystem.subsystem import scheduler


class System(object):

    def __init__(self, additional_subsystems=[]):
        # TODO(samueldmq): subsystem2 below !!!
        subsystem_list = subsystem2.all + additional_subsystems

        self.subsystems = {s.name: s
                           for s in subsystem_list}
        self.inject_dependencies()

        self.scheduler = scheduler.Manager()
        self.schedule_jobs()

    def schedule_jobs(self):
        pass

    def inject_dependencies(self):
        api = lambda: None
        for name, subsystem in self.subsystems.items():
            setattr(api, name, subsystem.router.controller.manager)

        # Dependency injection
        for subsystem in self.subsystems.values():
            subsystem.router.controller.manager.api = api
