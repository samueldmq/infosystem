import flask
import json

from infosystem.common import exception
from infosystem.common.subsystem import manager


class Controller(flask.Blueprint):

    def __init__(self, entity_cls, specific_manager=None):
        super(Controller, self).__init__(entity_cls.get_name(),
                                         entity_cls.get_name())

        self.entity_cls = entity_cls
        if specific_manager:
            self.manager = specific_manager
        else:
            self.manager = manager.Manager(entity_cls)

        self.register_routes()

    @property
    def collection_url(self):
        return '/' + self.entity_cls.get_collection_name()

    @property
    def entity_url(self):
        return self.collection_url + '/<id>'

    def register_routes(self):
        if hasattr(self.manager, 'create'):
            self.add_url_rule(self.collection_url,
                              view_func=self.create, methods=['POST'])
        if hasattr(self.manager, 'get'):
            self.add_url_rule(self.entity_url,
                              view_func=self.get, methods=['GET'])
        if hasattr(self.manager, 'list'):
            self.add_url_rule(self.collection_url,
                              view_func=self.list, methods=['GET'])
        if hasattr(self.manager, 'update'):
            self.add_url_rule(self.entity_url,
                              view_func=self.update, methods=['PATCH'])
        if hasattr(self.manager, 'delete'):
            self.add_url_rule(self.entity_url,
                              view_func=self.delete, methods=['DELETE'])

    def create(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        data = flask.request.get_json()

        try:
            entity = self.manager.create(data)
        except exception.InfoSystemException as exc:
            return flask.Response(headers={'Access-Control-Allow-Origin': '*'},
                                  response=exc.message,
                                  status=exc.status)

        response = {self.entity_cls.get_name(): entity.to_dict()}

        return flask.Response(headers={'Access-Control-Allow-Origin': '*'},
                              response=json.dumps(response),
                              status=201,
                              mimetype="application/json")

    def get(self, id):
        try:
            entity = self.manager.get(id=id)
        except exception.InfoSystemException as exc:
            return flask.Response(headers={'Access-Control-Allow-Origin': '*'},
                                  response=exc.message,
                                  status=exc.status)

        response = {self.entity_cls.get_name(): entity.to_dict()}

        return flask.Response(headers={'Access-Control-Allow-Origin': '*'},
                              response=json.dumps(response),
                              status=200,
                              mimetype="application/json")

    def list(self):
        filters = {k: flask.request.args.get(k) for k in flask.request.args.keys()}
        #TODO(samueldmq): fix this to work in a better way
        for k,v in filters.items():
            if v == 'True':
                filters[k] = True
            elif v == 'False':
                filters[k] = False
        try:
            entities = self.manager.list(**filters)
        except exception.InfoSystemException as exc:
            return flask.Response(headers={'Access-Control-Allow-Origin': '*'},
                                  response=exc.message,
                                  status=exc.status)

        response = {self.entity_cls.get_collection_name(): [entity.to_dict()
                                                      for entity in entities]}

        return flask.Response(headers={'Access-Control-Allow-Origin': '*'},
                              response=json.dumps(response),
                              status=200,
                              mimetype="application/json")

    def update(self, id):
        data = flask.request.get_json()

        try:
           entity = self.manager.update(data, id=id)
        except exception.InfoSystemException as exc:
            return flask.Response(headers={'Access-Control-Allow-Origin': '*'},
                                  response=exc.message,
                                  status=exc.status)

        response = {self.entity_cls.get_name(): entity.to_dict()}

        return flask.Response(headers={'Access-Control-Allow-Origin': '*'},
                              response=json.dumps(response),
                              status=200,
                              mimetype="application/json")

    def delete(self, id):
        try:
            self.manager.delete(id=id)
        except exception.InfoSystemException as exc:
            return flask.Response(headers={'Access-Control-Allow-Origin': '*'},
                                  response=exc.message,
                                  status=exc.status)

        return flask.Response(headers={'Access-Control-Allow-Origin': '*'},
                              response=None,
                              status=204,
                              mimetype="application/json")
