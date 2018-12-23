from datetime import datetime
from infosystem.database import db
from infosystem.common.subsystem import entity


class Token(entity.Entity, db.Model):

    attributes = ['user_id']
    attributes += entity.Entity.attributes

    user_id = db.Column(db.CHAR(32), db.ForeignKey("user.id"), nullable=False)

    def __init__(self, id, user_id,
                 created_at=datetime.now(), created_by=user_id,
                 updated_at=None, updated_by=None):
        super().__init__(id, created_at, created_by, updated_at, updated_by)
        self.user_id = user_id
