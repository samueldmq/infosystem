import flask
import json
import uuid

from infosystem import config
from infosystem import system


config = config.cfg


def check_uuid4(uuid_str):
    try:
        return uuid.UUID(uuid_str, version=4)
    except ValueError:
        return False


def enforce(roles, entry):
    # FIXME(samueldmq): This reads the file every request
    with open(config.rbac.policy_file) as policy_file:
        policy = json.load(policy_file)

        if '*' in policy[entry]:
            return

        intersection = set(roles).intersection(policy[entry])
        if not intersection:
            return flask.Response(response=None, status=401)


UUID_REPR = '<id>'
POST_TOKEN = ('POST', '/tokens')


def protect():
    method = flask.request.environ['REQUEST_METHOD']
    path = flask.request.environ['PATH_INFO'].rstrip('/')

    if (method, path) == POST_TOKEN:
        return

    path_bits = [UUID_REPR if check_uuid4(i) else i for i in path.split('/')]
    normalized_path = '/'.join(path_bits)
    entry = method + ' ' + normalized_path

    id = flask.request.headers.get('token')

    if id:
        token = system.api.token.get(id=id)
        grants = system.api.grant.list(user_id=token.user_id)
        grants_ids = [g.role_id for g in grants]
        roles = system.api.role.list()

        user_roles = [r.name for r in roles if r.id in grants_ids]

        return enforce(user_roles, entry)

    return enforce([], entry)
