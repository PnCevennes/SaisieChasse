#coding: utf8

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime

import datetime
import json

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import inspect
from sqlalchemy.orm import class_mapper, ColumnProperty, RelationshipProperty
from geoalchemy2.shape import to_shape, from_shape
from geojson import Feature

from geoalchemy2 import Geometry

db = SQLAlchemy()


class serializableModel(db.Model):
    """
    Classe qui ajoute une méthode de transformation des données
    de l'objet en tableau json
    Paramètres :
       -
    """
    __abstract__ = True

    def as_dict(self, recursif=False, columns=()):
        """
        Méthode qui renvoie les données de l'objet sous la forme d'un dictionnaire
        :param recursif: Spécifie si on veut que les sous objet (relationship) soit égalament sérialisé
        :param columns: liste des columns qui doivent être prisent en compte
        """
        obj = {}
        if (not columns):
            columns = self.__table__.columns

        for prop in class_mapper(self.__class__).iterate_properties:
            if getattr(self, prop.key) is None:
                pass
            else:
                if (isinstance(prop, ColumnProperty) and (prop.key in columns)):
                    column = self.__table__.columns[prop.key]
                    if isinstance(column.type, (db.Date, db.DateTime, UUID)):
                        obj[prop.key] = str(getattr(self, prop.key))
                    elif isinstance(column.type, db.Numeric):
                        obj[prop.key] = float(getattr(self, prop.key))
                    elif not isinstance(column.type, Geometry):
                        obj[prop.key] = getattr(self, prop.key)
                if ((isinstance(prop, RelationshipProperty)) and (recursif)):
                    if hasattr(getattr(self, prop.key), '__iter__'):
                        obj[prop.key] = [
                            d.as_dict(recursif)
                            for d in getattr(self, prop.key)
                        ]
                    else:
                        if (getattr(getattr(self, prop.key), "as_dict", None)):
                            obj[prop.key] = getattr(self, prop.key).as_dict(recursif)

        return obj


class serializableGeoModel(serializableModel):
    __abstract__ = True

    def as_geofeature(self, geoCol, idCol, recursif=False, columns=()):
        """
        Méthode qui renvoie les données de l'objet sous la forme d'une Feature geojson
        :param geoCol : Nom de la colonne géométrie
        :param idCol : Nom de la colonne primary key
        :param recursif: Spécifie si on veut que les sous objet (relationship) soit égalament sérialisé
        :param columns: liste des columns qui doivent être prisent en compte
        """
        geometry = to_shape(getattr(self, geoCol))
        feature = Feature(
                id=getattr(self, idCol),
                geometry=geometry,
                properties=self.as_dict(recursif, columns)
            )
        return feature
