from infosystem.common.subsystem import entity
from infosystem.database import db 


class User(entity.Entity, db.Model):

    attributes = ['id', 'name', 'email', 'active']
    name = db.Column(db.String(80), nullable=False, unique=True)
    domain_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    active = db.Column(db.Boolean(), nullable=False)

    def __init__(self, id, name, domain_id, email, password, active=True):
        super(User, self).__init__(id)
        self.name = name
        self.domain_id = domain_id
        self.email = email
        self.password = password
        self.active = active
