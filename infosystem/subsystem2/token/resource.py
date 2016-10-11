from infosystem.common.subsystem import entity
from infosystem.database import db


class Token(entity.Entity, db.Model):

    attributes = ['id', 'user_id']
    user_id = db.Column(db.CHAR(32), db.ForeignKey("user.id"), nullable=False)

    def __init__(self, id, user_id):
        super(Token, self).__init__(id)
        self.user_id = user_id
