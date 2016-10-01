from infosystem.common.subsystem import controller
from infosystem.common.subsystem import manager
from infosystem.subsystem.route import entity


class Controller(controller.Controller):

    def __init__(self):
    	# TODO(samueldmq): only some routes should appear at HTTP API
        super(Controller, self).__init__(manager.Manager(entity.Route))
