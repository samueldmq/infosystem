import os
import uuid

from infosystem.common import authorization
from infosystem import database
from infosystem import system
from flask import Flask


app = Flask(__name__)
app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


database.db.init_app(app)
with app.app_context():
    database.db.drop_all()
    database.db.create_all()

    domain = system.subsystems['domain'].manager.create(data={'name': 'default'})
    user_data = {'name': 'admin', 'email':'admin@example.com', 'password':'123456',
                 'domain_id': domain.id}
    user = system.subsystems['user'].manager.create(data=user_data)
    role = system.subsystems['role'].manager.create(data={'domain_id': domain.id, 'name':'admin'})
    system.subsystems['grant'].manager.create(data={'user_id': user.id, 'role_id':role.id})


for subsystem in system.subsystems.values():
    app.register_blueprint(subsystem)


app.before_request(authorization.protect)


if __name__ == '__main__':
    app.run(debug=True)

def load_app():
    return app
