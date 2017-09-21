import flask
import os
import hashlib

from infosystem import database
from infosystem import request
from infosystem import subsystem as subsystem_module
from infosystem import scheduler


ROUTES = [
    ('POST', '/users/reset'),
    ('GET', '/users/<id>'),
    ('GET', '/users/routes')
]


class System(flask.Flask):

    request_class = request.Request

    def __init__(self, *args, **kwargs):
        super().__init__(__name__, static_folder=None)

        self.configure()
        self.init_database()

        subsystem_list = subsystem_module.all + list(
            kwargs.values()) + list(args)

        self.subsystems = {s.name: s for s in subsystem_list}
        self.inject_dependencies()

        for subsystem in self.subsystems.values():
            self.register_blueprint(subsystem)

        # Add version in the root URL
        self.add_url_rule('/', view_func=self.version, methods=['GET'])

        self.scheduler = scheduler.Scheduler()
        self.schedule_jobs()

        self.bootstrap()

        self.before_request(
            request.RequestManager(self.subsystems).before_request)

    def configure(self):
        self.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
        self.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        self.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    def init_database(self):
        database.db.init_app(self)
        with self.app_context():
            database.db.create_all()

    def version(self):
        return '1.0.0'

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
            if not self.subsystems['domains'].manager.list():
                # Register default domain
                domain = self.subsystems['domains'].manager.create(
                    name='default')

                role = self.subsystems['roles'].manager.create(
                    name='admin', domain_id=domain.id)

                pass256 = hashlib.sha256(b"123456").hexdigest()
                user = self.subsystems['users'].manager.create(
                    domain_id=domain.id, name='sysadmin', password=pass256,
                    email="sysadmin@example.com")
                self.subsystems['grants'].manager.create(
                    user_id=user.id, role_id=role.id)

                # Register all system routes and all non-admin
                # routes as capabilities in the default domain
                for subsystem in self.subsystems.values():
                    for route in subsystem.router.routes:
                        bypass_param = route.get('bypass', False)
                        route_ref = self.subsystems['routes'].manager.create(
                            name=route['action'], url=route['url'],
                            method=route['method'], bypass=bypass_param)
                        # TODO(samueldmq): duplicate the line above here and
                        # see what breaks, it's probably the SQL
                        # session management!
                        if not route_ref.sysadmin:
                            cap_mng = self.subsystems['capabilities'].manager
                            capability = cap_mng.create(
                                domain_id=domain.id, route_id=route_ref.id)
                            if (route_ref.method, route_ref.url) in ROUTES:
                                self.subsystems['policies'].manager.create(
                                    capability_id=capability.id,
                                    role_id=role.id)
