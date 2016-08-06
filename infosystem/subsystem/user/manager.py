from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation

import smtplib

class Forgot(operation.Operation):

    def send_confirmation(self, email):
        gmail_user = 'oliveira.francois@gmail.com'
        gmail_pwd = 'kjfksjdfkdsj'
        FROM = gmail_user
        recipient = 'fdoliveira@objetorelacional.com.br'
        TO = recipient if type(recipient) is list else [recipient]
        SUBJECT = 'TESTE ASSUNTO'
        TEXT = 'TESTE CORPO'

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
            print('successfully sent the mail')
        except:
            print('failed to send mail')


    def pre(self, data, **kwargs):
        # print(kwargs['email'])
        email = 'oliveira.francois@gmail.com'

        users = self.manager.api.user.list(email=email)
        if not users:
            return False

        self.user = users[0]
        self.user_id = self.user.id

        return self.user.is_stable()

    def do(self, session, **kwargs):
        # print(self.user_id)

        self.send_confirmation(self.user.email)

        user = self.driver.get(self.user_id, session=session)
        return user

class Manager(manager.Manager):

    def register_operations(self):
        self.create = operation.Create(self)
        self.get = operation.Get(self)
        self.list = operation.List(self)
        self.delete = operation.Delete(self)
        self.forgot = Forgot(self)
