from infosystem.common.subsystem import router

class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
        return super().routes + [
            {'action': 'restore', 'method': 'POST', 'url': self.collection_url + '/restore', 'callback': self.controller.restore},
            {'action': 'reset', 'method': 'POST', 'url': self.collection_url + '/reset', 'callback': self.controller.reset},
            # TODO(samueldmq): re-enable this !!
            {'action': 'capabilities', 'method': 'GET', 'url': self.collection_url + '/capabilities', 'callback': self.controller.capabilities},
        ]