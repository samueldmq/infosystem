from sqlalchemy import orm
from datetime import datetime
from infosystem.database import db
from infosystem.subsystem.tag import resource
from infosystem.common.subsystem import entity


class Notification(entity.Entity, db.Model):

    attributes = ['id', 'user_id', 'date', 'subject', 'body', 'read_date']

    user_id = db.Column(
        db.CHAR(32), db.ForeignKey("user.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    read_date = db.Column(db.Date, nullable=True)
    tags = orm.relationship(
        "NotificationTag", backref=orm.backref('notification'),
        cascade='delete,delete-orphan,save-update')

    def __init__(self, id, user_id, date, subject, body, read_date=None):
        super().__init__(id)
        self.user_id = user_id
        self.date = datetime.strptime(date, entity.DATETIME_FMT)
        self.subject = subject
        self.body = body
        if (read_date is not None):
            self.read_date = datetime.strptime(read_date, entity.DATETIME_FMT)

    @classmethod
    def embedded(cls):
        return ['tags']


class NotificationTag(resource.Tag, db.Model):

    attributes = ['label']

    notification_id = db.Column(
        db.CHAR(32), db.ForeignKey("notification.id"), nullable=False)

    def __init__(self, id, label, notification_id):
        super().__init__(id, label)
        self.notification_id = notification_id
