from infosystem.common.subsystem import router


class Router(router.Router):

    def __init__(self, controller, collection, routes=[]):
        super().__init__(controller, collection, routes)

    @property
    def routes(self):
        return super().routes + [
            {
                'action': 'createAdmin', 'method': 'POST',
                'url': self.collection_url + '/createAdmin',
                'callback': self.controller.createAdmin
            },
            {
                'action': 'createWithGrantedResources', 'method': 'POST',
                'url': self.collection_url + '/createWithGrantedResources',
                'callback': self.controller.createWithGrantedResources
            }
        ]
