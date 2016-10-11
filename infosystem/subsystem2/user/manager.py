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

        users = self.manager.api.user.list(email=email)
        if not users:
            raise exception.OperationBadRequest()

        self.user = users[0]
        self.user_id = self.user.id

        domains = self.manager.api.domain.list(name=domain_name)
        if not domains:
            raise exception.OperationBadRequest()

        self.domain_id = domains[0].id
        return True

    def do(self, session, **kwargs):
        token = self.manager.api.token.create(user=self.user)
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
        token = self.manager.api.token.get(id=self.token)
        self.manager.api.user.update(id=token.user_id, password=self.password)


class Capabilities(operation.Operation):

    def pre(self, **kwargs):
        self.token = flask.request.headers.get('token')

        if not (self.token):
            raise exception.OperationBadRequest()
        return True

    def do(self, session, **kwargs):
        token = self.manager.api.token.get(id=self.token)
        grants = self.manager.api.grant.list(user_id=token.user_id)
        grants_ids = [g.role_id for g in grants]
        roles = self.manager.api.role.list()

        user_roles_id = [r.id for r in roles if r.id in grants_ids]

        # FIXME(fdoliveira) Try to send user_roles_id as paramater on query
        policies = self.manager.api.policy.list()
        policies_capabilitys_id = [p.capability_id for p in policies if ((p.bypass) or (p.role_id == None) or (p.role_id in user_roles_id))]

        capabilities = self.manager.api.capability.list()

        policy_capabilities = [c for c in capabilities if c.id in policies_capabilitys_id]

        return policy_capabilities


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.restore = Restore(self)
        self.reset = Reset(self)
        # TODO(samueldmq): re-enable /users/<id>/capabilities
        # self.capabilities = Capabilities(self)
