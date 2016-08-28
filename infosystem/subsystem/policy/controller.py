from infosystem.common.subsystem import controller
from infosystem.common.subsystem import manager
from infosystem.subsystem.policy import entity


class Controller(controller.Controller):

    def __init__(self):
        super(Controller, self).__init__(manager.Manager(entity.Policy))
