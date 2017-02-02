#coding: utf8

from server import db


from sqlalchemy import DateTime

import datetime
import json

class serializableModel(db.Model):
    __abstract__ = True

    def as_dict(self, recursif=False):
        if recursif :
            return self.as_dict_withrelationships()
        d = {}
        for c in self.__table__.columns :
            if  isinstance(c.type, db.DateTime) and getattr(self, c.name):
                d[c.name] = str(getattr(self, c.name))
            else:
                d[c.name] = getattr(self, c.name)

        return d

    def as_dict_withrelationships(self):
        obj = self.as_dict()
        for key in self.__mapper__.relationships.keys() :
            if self.__mapper__.relationships[key].uselist :
                obj[key] = [ item.as_dict() for item in getattr(self, key)]
            else :
                obj[key] = getattr(self, key).as_dict()
        return obj
