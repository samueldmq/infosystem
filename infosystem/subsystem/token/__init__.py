from infosystem.common import subsystem
from infosystem.subsystem.token import manager
from infosystem.subsystem.token import resource
from infosystem.subsystem.token import router

subsystem = subsystem.Subsystem(resource=resource.Token,
                                manager=manager.Manager,
                                router=router.Router)
