import flask
import os

from infosystem import database
from infosystem import request
from infosystem import subsystem as subsystem_module
from infosystem import scheduler
from infosystem.common import exception


class System(flask.Flask):

    request_class = request.Request

    def __init__(self, **kwargs):
        super().__init__(__name__, static_folder=None)

        self.configure()

        subsystem_list = subsystem_module.all + list(kwargs.values())

        self.subsystems = {s.name: s for s in subsystem_list}
        self.inject_dependencies()

        for subsystem in self.subsystems.values():
            self.register_blueprint(subsystem)

        self.scheduler = scheduler.Scheduler()
        self.schedule_jobs()

        self.bootstrap()

        self.before_request(request.RequestManager(self.subsystems).before_request)

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
                        route_ref = self.subsystems['routes'].manager.create(name=route['action'], url=route['url'], method=route['method'], bypass=route.get('bypass', False))
                        # TODO(samueldmq): duplicate the line above here and see what breaks, it's probably the SQL session management!
                    except exception.DuplicatedEntity:
                        pass

                    if not route_ref.admin:
                        self.subsystems['capabilities'].manager.create(domain_id=domain.id, route_id=route_ref.id)

            self.subsystems['users'].manager.create(domain_id=domain.id, name='admin', password='123456', email="admin@example.com")
