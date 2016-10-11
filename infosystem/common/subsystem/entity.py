from datetime import date
from datetime import datetime

from infosystem.database import db


DATE_FMT = '%Y-%m-%d'
DATETIME_FMT = '%Y-%m-%dT%H:%M:%SZ'


class Entity(object):

    attributes = ['id']
    id = db.Column(db.CHAR(32), primary_key=True)

    def __init__(self, id):
        self.id = id

    @classmethod
    def individual(cls):
        return cls.__name__.lower()

    @classmethod
    def collection(cls):
        return cls.individual() + 's'

    def is_stable(self):
        return True

    def to_dict(self, stringify=True):
        d = {}

        for attr in self.__class__.attributes:
            value = getattr(self, attr)
            if stringify and isinstance(value, datetime):
                d[attr] = value.strftime(DATETIME_FMT)
            elif stringify and isinstance(value, date):
                d[attr] = value.strftime(DATE_FMT)
            else:
                d[attr] = value

        return d
