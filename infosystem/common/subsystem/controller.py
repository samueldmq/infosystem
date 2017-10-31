import flask
import json

from infosystem.common import exception
# TODO(samueldmq): find a better name to this
# from infosystem.common.subsystem import manager as m


class Controller(object):

    def __init__(self, manager, resource_wrap, collection_wrap):
        self.manager = manager
        self.resource_wrap = resource_wrap
        self.collection_wrap = collection_wrap

    def create(self):
        # if not flask.request.is_json:
        #     return flask.Response(
        #         response=exception.BadRequestContentType.message,
        #         status=exception.BadRequestContentType.status)

        data = flask.request.get_json()

        try:
            if data:
                entity = self.manager.create(**data)
            else:
                entity = self.manager.create()
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.resource_wrap: entity.to_dict()}

        return flask.Response(response=json.dumps(response, default=str),
                              status=201,
                              mimetype="application/json")

    def get(self, id):
        try:
            entity = self.manager.get(id=id)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        response = {self.resource_wrap: entity.to_dict()}

        return flask.Response(response=json.dumps(response, default=str),
                              status=200,
                              mimetype="application/json")

    def _get_include_dict(self, query_arg, filter_args):
        lists = [l.split('.') for l in query_arg.split(',')]
        include_dict = {}
        for list in lists:
            current = include_dict
            for i in range(len(list)):
                if list[i] in current:
                    current[list[i]].update({
                        list[i + 1]: {}} if i < (len(list) - 1) else {})
                else:
                    current[list[i]] = {
                        list[i + 1]: {}} if i < (len(list) - 1) else {}
                current = current[list[i]]

        for k, v in filter_args.items():
            list = k.split('.')
            current = include_dict
            for i in list[:-1]:  # last element is the attribute to filter on
                try:
                    current = current[i]
                except AttributeError:
                    # ignore current filter,
                    # entity to filter on is not included
                    continue
            current[list[-1]] = v
        return include_dict

    def list(self):
        filters = {
            k: flask.request.args.get(k) for k in flask.request.args.keys()}
        # TODO(samueldmq): fix this to work in a better way
        for k, v in filters.items():
            if v == 'true':
                filters[k] = True
            elif v == 'false':
                filters[k] = False
            elif v == 'null':
                filters[k] = None

        include_arg = filters.pop('include', None)
        filter_args = {k: v for k, v in filters.items() if '.' in k}
        # clean up original filters
        for k in filter_args.keys():
            # NOTE(samueldmq): I'm not sure I can pop
            # in the list comprehesion above...
            filters.pop(k)

        try:
            entities = self.manager.list(**filters)
        except exception.InfoSystemException as exc:
            return flask.Response(response=exc.message,
                                  status=exc.status)

        include_dict = self._get_include_dict(
            include_arg, filter_args) if include_arg else {}
        collection = []
        for entity in entities:
            if isinstance(entity, dict):
                collection.append(entity)
            else:
                try:
                    collection.append(
                        entity.to_dict(include_dict=include_dict))
                except AssertionError:
                    # ignore current entity, filter mismatch
                    pass

        response = {self.collection_wrap: collection}

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

        return flask.Response(response=json.dumps(response, default=str),
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
