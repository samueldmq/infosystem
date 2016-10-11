import flask
import json

from infosystem.common import exception
# TODO(samueldmq): find a better name to this
from infosystem.common.subsystem import manager as m


class Controller(object):

    def __init__(self, manager, resource_wrap, collection_wrap):
        self.manager = manager
        self.resource_wrap = resource_wrap
        self.collection_wrap = collection_wrap

    def create(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        data = flask.request.get_json()

        try:
            entity = self.manager.create(**data)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.resource_wrap: entity.to_dict()}

        return flask.Response(response=json.dumps(response),
                              status=201,
                              mimetype="application/json")

    def get(self, id):
        try:
            entity = self.manager.get(id=id)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.resource_wrap: entity.to_dict()}

        return flask.Response(response=json.dumps(response),
                              status=200,
                              mimetype="application/json")

    def list(self):
        filters = {k: flask.request.args.get(k) for k in flask.request.args.keys()}
        #TODO(samueldmq): fix this to work in a better way
        for k,v in filters.items():
            if v == 'true':
                filters[k] = True
            elif v == 'false':
                filters[k] = False
            elif v == 'null':
                filters[k] = None
        try:
            entities = self.manager.list(**filters)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.collection_wrap: (
            [entity if isinstance(entity, dict) else entity.to_dict()
            for entity in entities])}

        return flask.Response(response=json.dumps(response, default=str),
                              status=200,
                              mimetype="application/json")

    def update(self, id):
        data = flask.request.get_json()

        try:
           entity = self.manager.update(**data)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.resource_wrap: entity.to_dict()}

        return flask.Response(response=json.dumps(response),
                              status=200,
                              mimetype="application/json")

    def delete(self, id):
        try:
            self.manager.delete(id=id)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")
