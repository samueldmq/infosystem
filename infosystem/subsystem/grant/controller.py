from infosystem.common.subsystem import controller
from infosystem.subsystem.grant import entity
from infosystem.subsystem.grant import manager


class Controller(controller.Controller):

    def __init__(self):
        super(Controller, self).__init__(entity.Grant,
                                         manager.Manager(entity.Grant))
