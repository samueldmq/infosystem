from infosystem.common.subsystem import entity
from infosystem.database import db


class Role(entity.Entity, db.Model):

    attributes = ['id', 'name', 'domain_id']
    name = db.Column(db.String(80), nullable=False, unique=True)
    domain_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)

    def __init__(self, id, name, domain_id):
        super(Role, self).__init__(id)
        self.name = name
        self.domain_id = domain_id
