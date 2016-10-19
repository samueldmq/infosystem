import json
import flask

from infosystem.common import exception
from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation

import smtplib


class Restore(operation.Operation):

    def pre(self, **kwargs):
        domain_name = kwargs.get('domain_name', None)
        email = kwargs.get('email', None)
        self.reset_url = kwargs.get('reset_url', None)

        if not (domain_name and email and self.reset_url):
            raise exception.OperationBadRequest()

        users = self.manager.api.users.list(email=email)
        if not users:
            raise exception.OperationBadRequest()

        self.user = users[0]
        self.user_id = self.user.id

        domains = self.manager.api.domains.list(name=domain_name)
        if not domains:
            raise exception.OperationBadRequest()

        self.domain_id = domains[0].id
        return True

    def do(self, session, **kwargs):
        token = self.manager.api.tokens.create(user=self.user)
        token_id = token.id

        from_email = 'oliveira.francois@gmail.com'
        recipient = self.user.email
        to_email = recipient if type(recipient) is list else [recipient]
        SUBJECT = 'TESTE ASSUNTO'
        TEXT = self.reset_url + '?token=' + token_id

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (from_email, ", ".join(to_email), SUBJECT, TEXT)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(from_email, '?')
            server.sendmail(from_email, to_email, message)
            server.quit()
        except:
            # TODO(samueldmq): do something here!
            pass


class Reset(operation.Operation):

    def pre(self, **kwargs):
        self.token = flask.request.headers.get('token')
        self.password = kwargs.get('password')

        if not (self.token and self.password):
            raise exception.OperationBadRequest()
        return True

    def do(self, session, **kwargs):
        token = self.manager.api.tokens.get(id=self.token)
        self.manager.api.users.update(id=token.user_id, password=self.password)


class Capabilities(operation.Operation):

    def pre(self, **kwargs):
        self.token = flask.request.headers.get('token')

        if not (self.token):
            raise exception.OperationBadRequest()
        return True

    def do(self, session, **kwargs):
        token = self.manager.api.tokens.get(id=self.token)
        grants = self.manager.api.grants.list(user_id=token.user_id)
        grants_ids = [g.role_id for g in grants]
        roles = self.manager.api.roles.list()

        user_roles_id = [r.id for r in roles if r.id in grants_ids]

        # FIXME(fdoliveira) Try to send user_roles_id as paramater on query
        policies = self.manager.api.policies.list()
        policies_capabilitys_id = [p.capability_id for p in policies if p.role_id in user_roles_id]

        user = self.manager.api.users.list(id=token.user_id)[0]
        capabilities = self.manager.api.capabilities.list(domain_id=user.domain_id)

        policy_capabilities = [c for c in capabilities if c.id in policies_capabilitys_id]

        # NOTE(samueldmq): if there is no policy for a capabiltiy, then it's open! add it too!
        restricted_capabilities = [p.capability_id for p in policies]
        open_capabilities = [c for c in capabilities if c.id not in restricted_capabilities]

        # TODO(samueldmq): should we return bypass routes too ? how if it is a list of capabilities ?

        return policy_capabilities + open_capabilities


class Routes(operation.Operation):

    def do(self, session, user_id, **kwargs):
        grants = self.manager.api.grants.list(user_id=user_id)
        grants_ids = [g.role_id for g in grants]
        roles = self.manager.api.roles.list()

        user_roles_id = [r.id for r in roles if r.id in grants_ids]

        # FIXME(fdoliveira) Try to send user_roles_id as paramater on query
        policies = self.manager.api.policies.list()
        policies_capabilitys_id = [p.capability_id for p in policies if p.role_id in user_roles_id]

        user = self.manager.api.users.list(id=user_id)[0]
        capabilities = self.manager.api.capabilities.list(domain_id=user.domain_id)

        policy_capabilities = [c for c in capabilities if c.id in policies_capabilitys_id]

        # NOTE(samueldmq): if there is no policy for a capabiltiy, then it's open! add it too!
        restricted_capabilities = [p.capability_id for p in policies]
        open_capabilities = [c for c in capabilities if c.id not in restricted_capabilities]

        user_routes = [self.manager.api.routes.get(id=c.route_id) for c in (policy_capabilities + open_capabilities)]

        bypass_routes = self.manager.api.routes.list(bypass=True)

        return list(set(user_routes).union(set(bypass_routes)))


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.restore = Restore(self)
        self.reset = Reset(self)
        self.capabilities = Capabilities(self)
        self.routes = Routes(self)
