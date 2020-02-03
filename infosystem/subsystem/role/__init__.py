from infosystem.common import subsystem
from infosystem.subsystem.role \
    import resource, router, controller, manager

subsystem = subsystem.Subsystem(resource=resource.Role,
                                router=router.Router,
                                controller=controller.Controller,
                                manager=manager.Manager)
