from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity
from infosystem.database import db


class Policy(entity.Entity, db.Model):

    attributes = ['id', 'capability_id', 'role_id', 'bypass']
    domain_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    capability_id = db.Column(db.CHAR(32), db.ForeignKey("capability.id"), nullable=False)
    role_id = db.Column(db.CHAR(32), db.ForeignKey("role.id"), nullable=True)
    bypass = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (UniqueConstraint('domain_id', 'capability_id', 'role_id', name='policy_uk'),)

    def __init__(self, id, domain_id, capability_id, role_id=None, bypass=False):
        super(Policy, self).__init__(id)
        self.domain_id = domain_id
        self.capability_id = capability_id
        self.role_id = role_id
        self.bypass = bypass
