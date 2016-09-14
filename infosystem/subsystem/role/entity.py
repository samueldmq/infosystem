from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity
from infosystem.database import db


class Role(entity.Entity, db.Model):

    attributes = ['id', 'name', 'active']
    domain_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)
    UniqueConstraint('domain_id', 'name', name='role_name_uk')

    def __init__(self, id, name, domain_id, active=True):
        super(Role, self).__init__(id)
        self.name = name
        self.domain_id = domain_id
        self.active = active
