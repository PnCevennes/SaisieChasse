#coding: utf8
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import ForeignKey, Sequence
from ..utils.genericmodels import serializableModel

db = SQLAlchemy()
class Thesaurus(serializableModel, db.Model):
    __tablename__ = 'tthesaurus'
    __table_args__ = {'schema':'chasse'}
    id = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.Integer)
    code = db.Column(db.Unicode)
    libelle = db.Column(db.Unicode)
    description = db.Column(db.Unicode)
    fk_parent = db.Column(db.Integer)
    hierarchie = db.Column(db.Unicode)
