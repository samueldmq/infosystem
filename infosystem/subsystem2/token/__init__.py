from infosystem.common import subsystem
from infosystem.subsystem2.token import manager
from infosystem.subsystem2.token import resource
from infosystem.subsystem2.token import router

subsystem = subsystem.Subsystem(resource=resource.Token,
                                manager=manager.Manager,
                                router=router.Router)
