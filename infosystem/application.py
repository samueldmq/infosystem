import flask
import os
import uuid
from flask import url_for
import urllib
import re

from infosystem.common import authorization
from infosystem import database
from infosystem import system as system_module


app = flask.Flask(__name__, static_folder=None)
app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SERVER_NAME'] = 'infosystem.com'

system = system_module.System()

database.db.init_app(app)

for subsystem in system.subsystems.values():
    app.register_blueprint(subsystem)


def bootstrap(app, system):
    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = '<' + arg +  '>'

        url = urllib.parse.unquote(url_for(rule.endpoint, **options))
        url = re.sub(".*" + app.config['SERVER_NAME'],"",url)
        methods = rule.methods
        try:
            # TODO(samueldmq): revisit this. Don't we really want HEAD ?
            methods.remove('HEAD')
        except KeyError:
            pass

        try:
            methods.remove('OPTIONS')
        except KeyError:
            pass

        for method in rule.methods:
            print(method, url)


with app.app_context():
    database.db.create_all()

    domain = system.subsystems['domain'].manager.create(data={'name': 'default'})
    user_data = {'name': 'admin', 'email':'admin@example.com', 'password':'123456',
                 'domain_id': domain.id}
    user = system.subsystems['user'].manager.create(data=user_data)
    role = system.subsystems['role'].manager.create(data={'domain_id': domain.id, 'name':'admin'})
    system.subsystems['grant'].manager.create(data={'user_id': user.id, 'role_id':role.id})

    bootstrap(app, system)


def protect():
    return authorization.protect(system)

app.before_request(protect)

def load_app():
    return app
