from infosystem.database import db
from infosystem.common.subsystem import entity


class Tag(entity.Entity):

    attributes = ['id', 'label']

    label = db.Column(db.String(50), nullable=False)

    def __init__(self, id, label):
        super().__init__(id)
        self.label = label
