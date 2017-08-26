from infosystem.common.subsystem import entity
from infosystem.database import db


class Policy(entity.Entity, db.Model):

    attributes = ['id', 'capability_id', 'role_id']
    capability_id = db.Column(db.CHAR(32), db.ForeignKey("capability.id"), nullable=False)
    role_id = db.Column(db.CHAR(32), db.ForeignKey("role.id"), nullable=False)

    def __init__(self, id, capability_id, role_id):
        super(Policy, self).__init__(id)
        self.capability_id = capability_id
        self.role_id = role_id

    @classmethod
    def collection(cls):
        return 'policies'
