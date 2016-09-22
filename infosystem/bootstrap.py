from flask import url_for
import urllib
import re
from infosystem.common import exception

exceptions = {('POST', '/tokens'): 'bypass'}


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
            capability = {'name': 'capability', 'method': method, 'url': url}
            try:
                system.subsystems['capability'].manager.create(**capability)
            except exception.DuplicatedEntity:
                pass # simply ignore if the capability is already registered

    capabilities = system.subsystems['capability'].manager.list()
    domains = system.subsystems['domain'].manager.list()

    for domain in domains:
        roles = system.subsystems['role'].manager.list(domain_id=domain.id,
                                                       name='admin')
        admin_role_id = roles[0].id
        for capability in capabilities:
            rule = 'admin'
            if (capability.method, capability.url) in exceptions:
                rule = exceptions[(capability.method, capability.url)]

            policy = {'domain_id': domain.id,
                      'capability_id': capability.id}
            if rule == 'admin':
                policy['role_id'] = admin_role_id
            elif rule == 'all':
                pass
            elif rule == 'bypass':
                policy['bypass'] = True
            else:
                # TODO(samueldmq): decide what to do here, it's a
                # programming error
                raise Exception('internal error')

            try:
                system.subsystems['policy'].manager.create(**policy)
            except exception.DuplicatedEntity:
                pass # simply ignore if the policy is already registered
