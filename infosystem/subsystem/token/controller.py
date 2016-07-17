from infosystem.common.subsystem import controller
from infosystem.subsystem.token import entity
from infosystem.subsystem.token import manager


class Controller(controller.Controller):

    def __init__(self):
        super(Controller, self).__init__(manager.Manager(entity.Token))
