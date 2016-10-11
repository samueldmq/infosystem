import flask
import os
import uuid

from flask import url_for
import urllib
import re


from infosystem.common import authorization
from infosystem.common import exception
from infosystem import database
from infosystem.bootstrap import *
# TODO(samueldmq): find a better name to this. aslo, it's system2 !!!
from infosystem import system2 as system_module


app = flask.Flask(__name__, static_folder=None)
app.config['BASEDIR'] = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SERVER_NAME'] = 'infosystem.com'

system = system_module.System()

database.db.init_app(app)

for subsystem in system.subsystems.values():
    app.register_blueprint(subsystem)

with app.app_context():
    database.db.create_all()
    system.bootstrap()


# def protect():
#     return authorization.protect(system)

# app.before_request(protect)

def load_app():
    return app
