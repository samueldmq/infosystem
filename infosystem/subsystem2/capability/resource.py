from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity
from infosystem.database import db


class Capability(entity.Entity, db.Model):

    attributes = ['id', 'route_id', 'domain_id']
    route_id = db.Column(db.CHAR(32), db.ForeignKey("route.id"), nullable=False)
    domain_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    __table_args__ = (UniqueConstraint('route_id', 'domain_id', name='capability_uk'),)

    def __init__(self, id, route_id, domain_id):
        super().__init__(id)
        self.route_id = route_id
        self.domain_id = domain_id

    @classmethod
    def collection(cls):
        return 'capabilities'
