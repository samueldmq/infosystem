from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity
from infosystem.database import db


class Share(entity.Entity, db.Model):

    attributes = ['id', 'capability_id', 'domain_id']
    capability_id = db.Column(db.CHAR(32), db.ForeignKey("capability.id"), nullable=False)
    domain_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    __table_args__ = (UniqueConstraint('capability_id', 'domain_id', name='share_uk'),)

    def __init__(self, id, capability_id, domain_id):
        super().__init__(id)
        self.capability_id = capability_id
        self.domain_id = domain_id
