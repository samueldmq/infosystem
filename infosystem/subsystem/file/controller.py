import flask

from infosystem.common import exception
from infosystem.common.subsystem import controller


# TODO(samueldmq): take a better look at this, it is completely different as it
# is not dealing with JSON content
class Controller(controller.Controller):

    def create(self):
        # TODO(samueldmq): the file should be extracted here.
        # the todo above would be resolved too with this!
        try:
            self.manager.create()
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=201,
                              mimetype="application/json")
