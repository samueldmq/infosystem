from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity
from infosystem.database import db


class Route(entity.Entity, db.Model):

    # TODO(samueldmq): recheck string lengths for below attributes
    # TODO(samueldmq): add an 'active' attribute
    attributes = ['id', 'name', 'url', 'method', 'sysadmin', 'bypass']
    name = db.Column(db.String(20), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    sysadmin = db.Column(db.Boolean(), nullable=False)
    bypass = db.Column(db.Boolean(), nullable=False)
    __table_args__ = (UniqueConstraint('url', 'method', name='route_uk'),)

    def __init__(self, id, name, url, method, sysadmin=False, bypass=False):
        self.id = id
        self.name = name
        self.url = url
        self.method = method
        self.method = method
        self.bypass = bypass
        self.sysadmin = sysadmin
