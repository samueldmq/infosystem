from infosystem.database import db
from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity


class Share(entity.Entity, db.Model):

    attributes = ['capability_id', 'domain_id']
    attributes += entity.Entity.attributes

    capability_id = db.Column(
        db.CHAR(32), db.ForeignKey("capability.id"), nullable=False)
    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint('capability_id', 'domain_id', name='share_uk'),)

    def __init__(self, id, capability_id, domain_id, active=True,
                 created_at=None, created_by=None,
                 updated_at=None, updated_by=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by)
        self.capability_id = capability_id
        self.domain_id = domain_id
