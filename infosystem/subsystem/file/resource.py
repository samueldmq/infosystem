from infosystem.database import db
from infosystem.common.subsystem import entity


class File(entity.Entity, db.Model):

    # This is required because Oracle dont accept FILE for table name
    __tablename__ = 'file_infosys'

    attributes = ['id', 'domain_id', 'name']

    domain_id = db.Column(
        db.CHAR(32), db.ForeignKey("domain.id"), nullable=True)
    name = db.Column(db.String(100), nullable=True)

    def __init__(self, id, domain_id, name):
        super().__init__(id)
        self.domain_id = domain_id
        self.name = name
