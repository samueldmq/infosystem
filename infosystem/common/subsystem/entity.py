from datetime import date
from datetime import datetime

from infosystem.database import db

DATE_FMT = '%Y-%m-%d'
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
        include_dict.update({attr: {} for attr in self.embedded()})
        if include_dict:
            for key, value in include_dict.items():
                if not isinstance(value, dict):
                    # it's a filter
                    if getattr(self, key) != value:
                        raise AssertionError()
                    continue

                thing = getattr(self, key)
                if isinstance(thing, list):
                    values = []
                    empty = True
                    for part in thing:
                        try:
                            values.append(part.to_dict(value))
                            empty = False
                        except AssertionError:
                            # filter mismatch, ignore the expansion
                            pass
                    if values and empty:
                        # filter mismatch, no entity matched the filter,
                        # re-raise and ignore current entity
                        raise AssertionError()
                    d[key] = [part.to_dict(value) for part in thing]
                else:
                    try:
                        d[key] = thing.to_dict(value)
                    except AssertionError:
                        # filter mismatch, re-raise to ignore current entity
                        raise

        return d
