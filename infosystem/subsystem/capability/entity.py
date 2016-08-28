from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity
from infosystem.database import db


class Capability(entity.Entity, db.Model):

    attributes = ['id', 'domain_id', 'policy_id', 'role_id']
    domain_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    policy_id = db.Column(db.CHAR(32), db.ForeignKey("policy.id"), nullable=False)
    role_id = db.Column(db.CHAR(32), db.ForeignKey("role.id"), nullable=False)
    UniqueConstraint('domain_id', 'policy_id', 'role_id', name='capability_uk')

    def __init__(self, id, domain_id, policy_id, role_id):
        super(Capabiliy, self).__init__(id)
        self.domain_id = domain_id
        self.policy_id = policy_id
        self.role_id = role_id
