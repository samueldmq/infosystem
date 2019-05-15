from infosystem.database import db
from infosystem.common.subsystem import entity


class Tag(entity.Entity):

    attributes = ['tag']

    tag = db.Column(db.String(50), nullable=False)

    def __init__(self, id, tag,
                 active=True, created_at=None, created_by=None,
                 updated_at=None, updated_by=None):
        super().__init__(id, active, created_at, created_by,
                         updated_at, updated_by)
        self.tag = tag
