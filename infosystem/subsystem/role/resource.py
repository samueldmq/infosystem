from infosystem.database import db
from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity


class Role(entity.Entity, db.Model):

    attributes = ['id', 'domain_id', 'name', 'active']

    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    __table_args__ = (
        UniqueConstraint('domain_id', 'name', name='role_name_uk'),)

    def __init__(self, id, domain_id, name, active=True):
        super().__init__(id)
        self.domain_id = domain_id
        self.name = name
        self.active = active
