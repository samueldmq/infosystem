import flask
import json
import uuid

from infosystem.common import exception

UUID_REPR = '<id>'

def check_uuid4(uuid_str):
    try:
        return uuid.UUID(uuid_str, version=4)
    except ValueError:
        return False

def unforce(system, path, method):
    capabilities = system.subsystems['capability'].manager.list(url=path, method=method)

    if len(capabilities) > 0:
        capability = capabilities[0]
    else:
        return flask.Response(response=None, status=401)

    policies = system.subsystems['policy'].manager.list(capability_id=capability.id, bypass=True)    
    if len(policies) > 0:
        return 
    else:
        return flask.Response(response=None, status=401)

def enforce(system, user_roles_id, path, method):
    capabilities = system.subsystems['capability'].manager.list(url=path, method=method)

    if len(capabilities) > 0:
        capability = capabilities[0]
    else:
        return flask.Response(response=None, status=401)

    policies = system.subsystems['policy'].manager.list(capability_id=capability.id, role_id=None)    
    if len(policies) > 0:
        return 

    policies = system.subsystems['policy'].manager.list(capability_id=capability.id)
    policies_roles_id = [p.role_id for p in policies]

    intersection = set(user_roles_id).intersection(policies_roles_id)
    if not intersection:
        return flask.Response(response=None, status=401)

    return

def protect(system):
    method = flask.request.environ['REQUEST_METHOD']
    original_path = flask.request.environ['PATH_INFO'].rstrip('/')

    path_bits = [UUID_REPR if check_uuid4(i) else i for i in original_path.split('/')]
    path = '/'.join(path_bits)

    id = flask.request.headers.get('token')

    if id:
        try:
            token = system.subsystems['token'].manager.get(id=id)
        except exception.NotFound:
            return flask.Response(response=None, status=401)

        grants = system.subsystems['grant'].manager.list(user_id=token.user_id)
        grants_ids = [g.role_id for g in grants]
        roles = system.subsystems['role'].manager.list()

        user_roles_id = [r.id for r in roles if r.id in grants_ids]

        return enforce(system, user_roles_id, path, method)

    return unforce(system, path, method)
