from datetime import date
from datetime import datetime

from infosystem.database import db


DATETIME_FMT = '%Y-%m-%dT%H:%M:%S.%fZ'


class Entity(object):

    attributes = ['id']
    id = db.Column(db.CHAR(32), primary_key=True)

    def __init__(self, id):
        self.id = id

    @classmethod
    def embedded(cls):
        return []

    @classmethod
    def individual(cls):
        return cls.__name__.lower()

    @classmethod
    def collection(cls):
        return cls.individual() + 's'

    def is_stable(self):
        return True

    def to_dict(self, include_dict=None, stringify=True):
        d = {}

        for attr in self.__class__.attributes:
            value = getattr(self, attr)
            if stringify and isinstance(value, datetime):
                d[attr] = value.strftime(DATETIME_FMT)
            elif stringify and isinstance(value, date):
                d[attr] = value.strftime(DATETIME_FMT)
            else:
                d[attr] = value

        include_dict = include_dict or {}
        include_dict.update({attr: None for attr in self.embedded()})
        if include_dict:
            for key,value in include_dict.items():
                thing = getattr(self, key)
                if isinstance(thing, list):
                    d[key] = [part.to_dict(value) for part in thing]
                else:
                    d[key] = thing.to_dict(value)

        return d
