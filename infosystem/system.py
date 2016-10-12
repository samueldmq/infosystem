from infosystem import database

import os
import uuid

from infosystem import subsystem as subsystem_module
# TODO(samueldmq): bring scheduler back!
# from infosystem.subsystem import scheduler
from infosystem.common import exception

import flask
import os
import uuid

from flask import url_for
import urllib
import re


from infosystem.common import authorization
from infosystem.common import exception
from infosystem import database


class System(flask.Flask):

    def __init__(self, additional_subsystems=[]):
        super().__init__(__name__, static_folder=None)

        self.configure()

        subsystem_list = subsystem_module.all + additional_subsystems

        self.subsystems = {s.name: s for s in subsystem_list}
        self.inject_dependencies()

        for subsystem in self.subsystems.values():
            self.register_blueprint(subsystem)

        # self.scheduler = scheduler.Manager()
        self.schedule_jobs()

        self.bootstrap()

        # def protect():
        #     return authorization.protect(system)

        # app.before_request(protect)

    def configure(self):
        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

        database.db.init_app(self)
        with self.app_context():
            database.db.create_all()

    def schedule_jobs(self):
        pass

    def inject_dependencies(self):
        api = lambda: None
        for name, subsystem in self.subsystems.items():
            setattr(api, name, subsystem.router.controller.manager)

        # Dependency injection
        for subsystem in self.subsystems.values():
            subsystem.router.controller.manager.api = api

    def bootstrap(self):
        """Bootstrap the system.

        - routes;
        - TODO(samueldmq): sysadmin;
        - default domain with admin and capabilities.

        """

        with self.app_context():
            # Register default domain
            domain = self.subsystems['domains'].manager.create(name='default')

            # Register all system routes and all non-admin routes as capabilities in the default domain
            for subsystem in self.subsystems.values():
                for route in subsystem.router.routes:
                    try:
                        route_ref = self.subsystems['routes'].manager.create(name=route['action'], url=route['url'], method=route['method'])
                        # TODO(samueldmq): duplicate the line above here and see what breaks, it's probably the SQL session management!
                    except exception.DuplicatedEntity:
                        pass

                    if not route_ref.admin:
                        self.subsystems['capabilities'].manager.create(domain_id=domain.id, route_id=route_ref.id)

            self.subsystems['users'].manager.create(domain_id=domain.id, name='admin', password='123456', email="admin@example.com")
