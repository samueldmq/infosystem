from infosystem.common import subsystem
from infosystem.subsystem.file import resource
from infosystem.subsystem.file import manager
from infosystem.subsystem.file import controller

subsystem = subsystem.Subsystem(resource=resource.File,
                                manager=manager.Manager,
                                controller=controller.Controller)
