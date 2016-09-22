import flask
import os
import uuid


from infosystem.common import authorization
from infosystem.common import exception
from infosystem import database
from infosystem.bootstrap import *
from infosystem import system as system_module


app = flask.Flask(__name__, static_folder=None)
app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SERVER_NAME'] = 'infosystem.com'

system = system_module.System()

database.db.init_app(app)

for subsystem in system.subsystems.values():
    app.register_blueprint(subsystem)


with app.app_context():
    database.db.create_all()

    domain = system.subsystems['domain'].manager.create(name='default')
    user_data = {'name': 'admin', 'email':'admin@example.com', 'password':'123456',
                 'domain_id': domain.id}
    user = system.subsystems['user'].manager.create(**user_data)
    role = system.subsystems['role'].manager.create(domain_id=domain.id, name='admin')
    system.subsystems['grant'].manager.create(user_id=user.id, role_id=role.id)

    bootstrap(app, system)


def protect():
    return authorization.protect(system)

app.before_request(protect)

def load_app():
    return app
