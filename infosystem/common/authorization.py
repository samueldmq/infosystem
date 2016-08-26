import flask
import json
import uuid

from infosystem import config
from infosystem.common import exception


config = config.cfg


def check_uuid4(uuid_str):
    try:
        return uuid.UUID(uuid_str, version=4)
    except ValueError:
        return False


def unforce(entry):
    # FIXME(samueldmq): This reads the file every request
    with open(config.rbac.policy_file) as policy_file:
        policy = json.load(policy_file)

        if '' in policy[entry]:
            return
        
        return flask.Response(response=None, status=401)

def enforce(roles, entry):
    # FIXME(samueldmq): This reads the file every request
    with open(config.rbac.policy_file) as policy_file:
        policy = json.load(policy_file)

        if '*' in policy[entry]:
            return

        if roles == None:
            return flask.Response(response=None, status=401)

        intersection = set(roles).intersection(policy[entry])
        if not intersection:
            return flask.Response(response=None, status=401)


UUID_REPR = '<id>'
POST_TOKEN = ('POST', '/tokens')


def protect(system):
    method = flask.request.environ['REQUEST_METHOD']
    path = flask.request.environ['PATH_INFO'].rstrip('/')

    if (method, path) == POST_TOKEN:
        return

    path_bits = [UUID_REPR if check_uuid4(i) else i for i in path.split('/')]
    normalized_path = '/'.join(path_bits)
    entry = method + ' ' + normalized_path

    id = flask.request.headers.get('token')

    if id:
        try:
            token = system.subsystems['token'].manager.get(id=id)
        except exception.NotFound:
            return flask.Response(response=None, status=401)

        grants = system.subsystems['grant'].manager.list(user_id=token.user_id)
        grants_ids = [g.role_id for g in grants]
        roles = system.subsystems['role'].manager.list()

        user_roles = [r.name for r in roles if r.id in grants_ids]

        return enforce(user_roles, entry)

    return unforce(entry)
