from infosystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
        # TODO(samueldmq): is this the best way to re-write the defaults to
        # only change bypass=true for create ?
        return [
            {
                'action': 'create',
                'method': 'POST',
                'url': self.collection_url,
                'callback': self.controller.create,
                'bypass': True
            },
            {
                'action': 'get',
                'method': 'GET',
                'url': self.resource_url,
                'callback': self.controller.get
            },
            {
                'action': 'delete',
                'method': 'DELETE',
                'url': self.resource_url,
                'callback': self.controller.delete
            }
        ]
