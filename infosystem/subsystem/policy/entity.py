from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity
from infosystem.database import db


class Policy(entity.Entity, db.Model):

    attributes = ['id', 'domain_id', 'capability_id', 'role_id']
    domain_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    capability_id = db.Column(db.CHAR(32), db.ForeignKey("capability.id"), nullable=False)
    role_id = db.Column(db.CHAR(32), db.ForeignKey("role.id"), nullable=False)
    UniqueConstraint('domain_id', 'capability_id', 'role_id', name='capability_uk')

    def __init__(self, id, domain_id, capability_id, role_id):
        super(Policy, self).__init__(id)
        self.domain_id = domain_id
        self.capability_id = capability_id
        self.role_id = role_id
