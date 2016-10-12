from infosystem.common import subsystem
from infosystem.subsystem.user import resource

from infosystem.subsystem.user import controller
from infosystem.subsystem.user import manager
from infosystem.subsystem.user import router


subsystem = subsystem.Subsystem(resource=resource.User,
                                router=router.Router,
                                controller=controller.Controller,
                                manager=manager.Manager)
