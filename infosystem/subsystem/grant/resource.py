from infosystem.database import db
from infosystem.common.subsystem import entity
from sqlalchemy import orm


class Grant(entity.Entity, db.Model):

    attributes = ['id', 'user_id', 'role_id']

    user_id = db.Column(db.CHAR(32), db.ForeignKey("user.id"), nullable=False)
    user = orm.relationship("User", backref=orm.backref('grants'))
    role_id = db.Column(db.CHAR(32), db.ForeignKey("role.id"), nullable=False)
    role = orm.relationship("Role", backref=orm.backref('grants'))

    def __init__(self, id, user_id, role_id):
        super().__init__(id)
        self.user_id = user_id
        self.role_id = role_id
