from infosystem.database import db
from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity


class Route(entity.Entity, db.Model):

    attributes = ['id', 'name', 'url', 'method', 'sysadmin', 'bypass']

    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(80), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    bypass = db.Column(db.Boolean(), nullable=False)
    sysadmin = db.Column(db.Boolean(), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    __table_args__ = (UniqueConstraint('url', 'method', name='route_uk'),)

    def __init__(
            self, id, name, url, method, bypass=False, sysadmin=False,
            active=True):
        self.id = id
        self.name = name
        self.url = url
        self.method = method
        self.bypass = bypass
        self.sysadmin = sysadmin
        self.active = active
