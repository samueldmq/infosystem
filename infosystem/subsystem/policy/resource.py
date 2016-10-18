from infosystem.common.subsystem import entity
from infosystem.database import db


class Policy(entity.Entity, db.Model):

    attributes = ['id', 'capability_id', 'role_id']
    capability_id = db.Column(db.CHAR(32), db.ForeignKey("capability.id"), nullable=False)
    role_id = db.Column(db.CHAR(32), db.ForeignKey("role.id"), nullable=False)

    def __init__(self, id, capability_id, role_id):
        super(Grant, self).__init__(id)
        self.user_id = user_id
        self.role_id = role_id

    @classmethod
    def collection(cls):
        return 'policies'
