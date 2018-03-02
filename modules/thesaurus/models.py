# coding: utf8
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import ForeignKey, Sequence
from ..utils.genericmodels import serializableModel

from modules.database import DB


class Thesaurus(serializableModel, DB.Model):
    __tablename__ = 'tthesaurus'
    __table_args__ = {'schema': 'chasse'}
    id = DB.Column(DB.Integer, primary_key=True)
    id_type = DB.Column(DB.Integer)
    code = DB.Column(DB.Unicode)
    libelle = DB.Column(DB.Unicode)
    description = DB.Column(DB.Unicode)
    fk_parent = DB.Column(DB.Integer)
    hierarchie = DB.Column(DB.Unicode)
