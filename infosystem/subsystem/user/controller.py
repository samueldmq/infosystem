# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import flask
import json

from infosystem.common import exception
from infosystem.common.subsystem import controller
from infosystem.subsystem.user import entity
from infosystem.subsystem.user import manager


class Controller(controller.Controller):

    def __init__(self):
        super(Controller, self).__init__(manager.Manager(entity.User))

    def register_routes(self):
        super(Controller, self).register_routes()

        self.add_url_rule('/users/restore', view_func=self.restore, methods=['POST'])
        self.add_url_rule('/users/reset', view_func=self.reset, methods=['POST'])

    # TODO(samueldmq): this method and the one just below can share code
    # TODO(samueldmq): make sure rbac works if open [""] and a token is passed!
    def restore(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        data = flask.request.get_json()

        try:
            entity = self.manager.restore(**data)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=200,
                              mimetype="application/json")

    def reset(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        data = flask.request.get_json()

        try:
            entity = self.manager.reset(data)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=200,
                              mimetype="application/json")
