from infosystem.common import subsystem
from infosystem.subsystem2.token import manager
from infosystem.subsystem2.token import resource

subsystem = subsystem.Subsystem(resource=resource.Token,
                                manager=manager.Manager,
                                operations=['create', 'get', 'delete'])
