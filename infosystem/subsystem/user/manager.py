import flask

from infosystem.common import exception
from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation
from infosystem.common import exception

import smtplib

class Restore(operation.Operation):

    def pre(self, data, **kwargs):
        domain_name = kwargs.get('domain_name')
        email = kwargs.get('email')
        self.reset_url = kwargs.get('reset_url')

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

        gmail_user = ''
        gmail_pwd = ''
        FROM = gmail_user
        recipient = ''
        TO = recipient if type(recipient) is list else [recipient]
        SUBJECT = 'TESTE ASSUNTO'
        TEXT = self.reset_url + '?token=' + token_id

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(gmail_user, gmail_pwd)
            server.sendmail(FROM, TO, message)
            server.close()
        except:
            # TODO(samueldmq): do something here!
            pass


class Reset(operation.Operation):

    def pre(self, data, **kwargs):
        self.token = flask.request.headers.get('token')
        self.password = data.get('password')

        if not (self.token and self.password):
            raise exception.OperationBadRequest()
        return True

    def do(self, session, **kwargs):
        token = self.manager.api.token.get(id=self.token)
        self.manager.api.user.update(id=token.user_id, data={'password': self.password})


class Manager(manager.Manager):

    def register_operations(self):
        self.create = operation.Create(self)
        self.get = operation.Get(self)
        self.list = operation.List(self)
        self.update = operation.Update(self)
        self.delete = operation.Delete(self)
        self.restore = Restore(self)
        self.reset = Reset(self)
