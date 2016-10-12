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


def check_uuid4(uuid_str):
    try:
        return uuid.UUID(uuid_str, version=4)
    except ValueError:
        return False


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

        self.before_request(self.prepare)
        self.before_request(self.route)
        self.before_request(self.protect)

    def prepare(self):
        """Extract route and domain info from request and add to context."""
        method = flask.request.environ['REQUEST_METHOD']
        original_path = flask.request.environ['PATH_INFO'].rstrip('/')

        path_bits = ['<id>' if check_uuid4(i) else i for i in original_path.split('/')]
        path = '/'.join(path_bits)

        flask.request.environ['method'] = method
        flask.request.environ['url'] = path

        id = flask.request.headers.get('token')

        if id:
            try:
                token = self.subsystems['tokens'].manager.get(id=id)
            except exception.NotFound:
                return flask.Response(response=None, status=401)

            user = self.subsystems['users'].manager.list(user_id=token.user_id)[0]
            flask.request.environ['user_id'] = user.id
            flask.request.environ['domain_id'] = user.domain_id
        else:
            flask.request.environ['user_id'] = None
            flask.request.environ['domain_id'] = None

    def route(self):
        # check if route is available @ current domain (capability or bypass route)

        url = flask.request.environ['url']
        method = flask.request.environ['method']
        domain_id = flask.request.environ['domain_id']

        routes = self.subsystems['routes'].manager.list(url=url, method=method)
        if not routes:
            return flask.Response(response=None, status=404)

        route = routes[0]
        capabilities = self.subsystems['capabilities'].manager.list(route_id=route.id, domain_id=domain_id)

        # TODO(samueldmq): sysadmin won't provide a domain, so capabilities will be empty
        # treat this case here once we support sysadmin
        if not capabilities:
            return flask.Response(response=None, status=404)

    def protect(self):
        url = flask.request.environ['url']
        method = flask.request.environ['method']
        domain_id = flask.request.environ['domain_id']
        user_id = flask.request.environ['user_id']

        route = self.subsystems['routes'].manager.list(url=url, method=method)[0]
        if route.bypass:
            return

        # check the current user has enough privilegies to access this route (roles or capability is open)
        print(flask.request.environ['url'])
        print(flask.request.environ['method'])
        print(flask.request.environ['user_id'])
        print(flask.request.environ['domain_id'])

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
