from infosystem.common.subsystem import entity
from infosystem.database import db 


class Domain(entity.Entity, db.Model):

    attributes = ['id', 'name', 'active']
    name = db.Column(db.String(80), nullable=False, unique=True)
    active = db.Column(db.Boolean(), nullable=False)

    def __init__(self, id, name, active=True):
        super(Domain, self).__init__(id)
        self.name = name
        self.active = active
