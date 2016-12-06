from infosystem.common.subsystem import entity
from infosystem.database import db


class File(entity.Entity, db.Model):

    attributes = ['id', 'domain_id', 'name']
    domain_id = db.Column(db.CHAR(32), db.ForeignKey("domain.id"), nullable=True)
    name = db.Column(db.String(100), nullable=True)
    __tablename__ = 'Files' # This is required because Oracle dont accept FILE for table name

    def __init__(self, id, domain_id, name):
        super(File, self).__init__(id)
        self.domain_id = domain_id
        self.name = name
