import flask
import json

from infosystem.common import exception
from infosystem.common.subsystem import manager


class Controller(flask.Blueprint):

    def __init__(self, manager):
        super(Controller, self).__init__(manager.entity_name,
                                         manager.entity_name)

        self.manager = manager
        self.register_routes()

    @property
    def collection_url(self):
        return '/' + self.manager.collection_name

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
                              view_func=self.update, methods=['PUT'])
        if hasattr(self.manager, 'delete'):
            self.add_url_rule(self.entity_url,
                              view_func=self.delete, methods=['DELETE'])

    def _determine_domain_id(self):
        token_id = flask.request.headers.get('token')
        if token_id:
            token = self.manager.api.token.get(id=token_id)
            user = self.manager.api.user.get(id=token.user_id)
            domain = self.manager.api.domain.get(id=user.domain_id)
            return domain.id

    def create(self):
        if not flask.request.is_json:
            return flask.Response(
                response=exception.BadRequestContentType.message,
                status=exception.BadRequestContentType.status)

        data = flask.request.get_json()
        domain_id = self._determine_domain_id()
        if domain_id:
            data['domain_id'] = domain_id
        else:
            pass #TODO(samueldmq): what to do here ?

        try:
            entity = self.manager.create(**data)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.manager.entity_name: entity.to_dict()}

        return flask.Response(response=json.dumps(response),
                              status=201,
                              mimetype="application/json")

    def get(self, id):
        # TODO(samueldmq): only return if the id belongs to _determine_domain_id()
        try:
            entity = self.manager.get(id=id)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.manager.entity_name: entity.to_dict()}

        return flask.Response(response=json.dumps(response),
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

        domain_id = self._determine_domain_id()
        if domain_id:
            filters['domain_id'] = domain_id
        else:
            pass #TODO(samueldmq): what to do here ?

        try:
            entities = self.manager.list(**filters)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.manager.collection_name: (
            [entity if isinstance(entity, dict) else entity.to_dict()
            for entity in entities])}

        return flask.Response(response=json.dumps(response, default=str),
                              status=200,
                              mimetype="application/json")

    def update(self, id):
        # TODO(samueldmq): only update if the id belongs to _determine_domain_id()
        data = flask.request.get_json()

        try:
           entity = self.manager.update(id=id, **data)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.manager.entity_name: entity.to_dict()}

        return flask.Response(response=json.dumps(response),
                              status=200,
                              mimetype="application/json")

    def delete(self, id):
        # TODO(samueldmq): only delete if the id belongs to _determine_domain_id()

        try:
            self.manager.delete(id=id)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        return flask.Response(response=None,
                              status=204,
                              mimetype="application/json")
