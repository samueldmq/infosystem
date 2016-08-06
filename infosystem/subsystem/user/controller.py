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

        self.add_url_rule('/forgot', view_func=self.forgot, methods=['GET'])

    def forgot(self):
        args = {k: flask.request.args.get(k) for k in flask.request.args.keys()}

        try:
            entity = self.manager.forgot(**args)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.manager.entity_name: entity.to_dict()}

        return flask.Response(response=json.dumps(response),
                              status=200,
                              mimetype="application/json")
