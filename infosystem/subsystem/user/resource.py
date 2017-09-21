import uuid
from sqlalchemy import orm
from infosystem.database import db
from sqlalchemy import UniqueConstraint
from infosystem.common.subsystem import entity


class User(entity.Entity, db.Model):

    attributes = ['id', 'domain_id', 'name', 'email', 'active']

    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    domain = orm.relationship("Domain", backref=orm.backref('users'))
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    __table_args__ = (
        UniqueConstraint('domain_id', 'name', name='user_name_uk'),
        UniqueConstraint('domain_id', 'email', name='user_email_uk'),)

    def __init__(
            self, id, domain_id, name, email,
            password=uuid.uuid4().hex, active=True):
        super().__init__(id)
        self.domain_id = domain_id
        self.name = name
        self.email = email
        self.password = password
        self.active = active
