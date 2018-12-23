from infosystem.database import db
from infosystem.common.subsystem import entity


class Domain(entity.Entity, db.Model):

    attributes = ['active', 'name', 'parent_id']
    attributes += entity.Entity.attributes

    active = db.Column(db.Boolean(), nullable=False)
    name = db.Column(db.String(60), nullable=False, unique=True)
    parent_id = db.Column(
        db.CHAR(32), db.ForeignKey("domain.id"), nullable=True)

    def __init__(self, id, name, active=True, parent_id=None,
                 created_at=None, created_by=None,
                 updated_at=None, updated_by=None):
        super().__init__(id, created_at, created_by, updated_at, updated_by)
        self.active = active
        self.name = name
        self.parent_id = parent_id
