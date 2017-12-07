from sqlalchemy import orm
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
        self.date = date
        self.subject = subject
        self.body = body
        self.read_date = read_date


class NotificationTag(resource.Tag, db.Model):

    notification_id = db.Column(
        db.CHAR(32), db.ForeignKey("notification.id"), nullable=False)

    def __init__(self, id, label, notification_id):
        super().__init__(id, label)
        self.notification_id = notification_id
