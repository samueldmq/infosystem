from infosystem.common.subsystem import entity
from infosystem.database import db


class Domain(entity.Entity, db.Model):

    attributes = ['id', 'active', 'name', 'parent_id']
    active = db.Column(db.Boolean(), nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    parent_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=True)

    def __init__(self, id, name, parent_id=None, active=True):
        super(Domain, self).__init__(id)
        self.active = active
        self.name = name
        self.parent_id = parent_id
