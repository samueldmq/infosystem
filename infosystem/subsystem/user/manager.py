import os
import hashlib
import smtplib
import flask


from infosystem.common import exception
from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation

_RESET_URL = 'http://ormob-ds.dyndns.org:8000/#/reset/'

_HTML_EMAIL = """
<!DOCTYPE html>
<html>
  <head>
    <title>Atualizar Senha</title>
  </head>
  <body>
    <div style="width: 100%; text-align: center">
      <h1>DISTRIBUIDORA DE ALIMENTOS SERIDÓ LTDA</h1>
      <h2>CONFIRMAR E CRIAR SENHA</h2>
    </div>

    <p>Você acaba de ser cadastrado no portal da Distribuidora de Alimentes Seridó LTDA.</p>
    <p>Para ter acesso ao sistema você deve clicar no link abaixo para confirmar esse email e criar uma senha.</p>

    <div style="width: 100%; text-align: center">
       <a href="{reset_link}">Clique aqui para CONFIRMAR o email e CRIAR uma senha.</a>
    </div>
  </body>
</html>
"""


def send_reset_password_email(token_id, reset_user, reset_url):
    from_email = 'infosystemcontact@gmail.com'
    recipient = reset_user.email
    to_email = recipient if type(recipient) is list else [recipient]
    SUBJECT = 'PORTAL DISTRIBUIDORA SERIDÓ - CONFIRMAR email e CRIAR senha'
    LINK = reset_url + '/' + token_id

    # Prepare actual message
    msg_header = 'From: %s\n' \
                    'To: %s\n' \
                    'MIME-Version: 1.0\n' \
                    'Content-type: text/html\n' \
                    'Subject: %s\n' \
                    % (from_email, ", ".join(to_email), SUBJECT)
    msg_content = _HTML_EMAIL.format(reset_link=LINK)
    msg_full = (''.join([msg_header, msg_content])).encode()

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(from_email, 'abc010203')
        server.sendmail(from_email, to_email, msg_full)
        server.quit()
    except:
        # TODO(samueldmq): do something here!
        pass


class Create(operation.Create):

    def do(self, session, **kwargs):
        self.entity = super().do(session, **kwargs)

        self.token = self.manager.api.tokens.create(user=self.entity)

        return self.entity

    def post(self):
        send_reset_password_email(self.token.id, self.entity, _RESET_URL)


class Update(operation.Update):

    def do(self, session, **kwargs):
        password = kwargs.get('password', None)
        if password:
            kwargs['password'] = hashlib.sha256(password.encode('utf-8')).hexdigest()

        self.entity = super().do(session, **kwargs)

        return self.entity


class Restore(operation.Operation):

    def pre(self, **kwargs):
        domain_name = kwargs.get('domain_name', None)
        email = kwargs.get('email', None)
        self.reset_url = kwargs.get('reset_url', _RESET_URL)

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
        send_reset_password_email(token.id, self.user, self.reset_url)


class Reset(operation.Operation):

    def pre(self, **kwargs):
        self.token = flask.request.headers.get('token')
        self.password = kwargs.get('password')

        if not (self.token and self.password):
            raise exception.OperationBadRequest()
        return True

    def do(self, session, **kwargs):
        token = self.manager.api.tokens.get(id=self.token)
        self.manager.update(id=token.user_id, password=self.password)

    def post(self):
        self.manager.api.tokens.delete(id=self.token)


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
        self.create = Create(self)
        self.update = Update(self)
        self.restore = Restore(self)
        self.reset = Reset(self)
        self.routes = Routes(self)
