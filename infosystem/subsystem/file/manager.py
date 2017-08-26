import flask
import uuid
import os
from werkzeug import utils as werkzeug_utils

from infosystem.common.subsystem import manager
from infosystem.common.subsystem import operation


# TODO(samueldmq): put this in the app config
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class Create(operation.Create):

    def pre(self, session, **kwargs):
        # TODO(samueldmq): replace with proper domain_id
        self.domain_id = self.manager.api.domains.list(name='default')[0].id

        self.file = flask.request.files.get('file', None)
        if self.file and allowed_file(self.file.filename):
            filename = werkzeug_utils.secure_filename(self.file.filename)
            self.entity = self.driver.instantiate(
                id=uuid.uuid4().hex, domain_id=self.domain_id, name=filename)
        else:
            # NOTE(samueldmq): this will force a 400 since the name is not
            # provided, raise specific exception here about the file
            self.entity = self.driver.instantiate(
                id=uuid.uuid4().hex, domain_id=self.domain_id)

        return self.entity.is_stable()

    def do(self, session, **kwargs):
        folder = os.path.join(UPLOAD_FOLDER, self.domain_id)
        if not os.path.exists(folder):
            os.makedirs(folder)
        self.file.save(os.path.join(folder, self.entity.name))
        super().do(session)


class Get(operation.Get):

    def do(self, session, **kwargs):
        file = super().do(session, **kwargs)

        folder = os.path.join(UPLOAD_FOLDER, file.domain_id)
        return flask.send_from_directory(folder, file.name)


class Manager(manager.Manager):

    def __init__(self, driver):
        super().__init__(driver)
        self.create = Create(self)
        self.get = Get(self)
