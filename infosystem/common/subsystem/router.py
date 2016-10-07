import flask


class Route(object):

    def __init__(self, name, method, url, callback):
        self.name = name
        self.method = method
        self.url = url
        self.callback = callback


class Router(object):

    def __init__(self, resource):
        super(Router, self).__init__(resource.collection, resource.collection)

        self.collection_url = '/' + resource.collection
        self.resource_url = self.collection_url + '/<id>'

    @property
    def routes(self):
        return [
            Route('Create ' + resource.collection, 'POST', self.collection_url, self.controller.create),
            Route('Get '    + resource.collection, 'GET',  self.resource_url,   self.controller.get),
            Route('List '   + resource.collection, 'GET',  self.collection_url, self.controller.list),
            Route('Update ' + resource.collection, 'PUT',  self.resource_url,   self.controller.update),
            Route('Delete ' + resource.collection, 'PUT',  self.resource_url,   self.controller.update)
        ]
