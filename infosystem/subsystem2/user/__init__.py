from infosystem.common import subsystem
from infosystem.subsystem2.user import resource

from infosystem.subsystem2.user import controller
from infosystem.subsystem2.user import manager
from infosystem.subsystem2.user import router


subsystem = subsystem.Subsystem(resource=resource.User,
                                router=router.Router,
                                controller=controller.Controller,
                                manager=manager.Manager)
