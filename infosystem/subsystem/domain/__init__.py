from infosystem.common import subsystem
from infosystem.subsystem.domain import manager, resource

subsystem = subsystem.Subsystem(resource=resource.Domain,
                                manager=manager.Manager)
