# coding: utf8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Sequence
from ..utils.genericmodels import serializableModel
from geoalchemy2 import Geometry


from . import db


class LieuTirSynonymes(serializableModel, db.Model):
    __tablename__ = 'lieu_tir_synonymes'
    __table_args__ = {'schema': 'chasse'}
    id = db.Column(db.Integer, primary_key=True)
    code_lieudit = db.Column(
        db.Integer,
        ForeignKey("chasse.lieux_tir.code_lieudit"),
        nullable=False
    )
    libelle_lieudit = db.Column(db.Unicode)


class VLieuTirSynonymes(serializableModel, db.Model):
    __tablename__ = 'v_lieu_dit_synonymes'
    __table_args__ = {'schema': 'chasse'}
    id = db.Column(db.Integer, primary_key=True)
    code_lieudit = db.Column(db.Integer)
    nom_lieudit = db.Column(db.Unicode)
    synonyme = db.Column(db.Unicode)
    code_com = db.Column(db.Integer)
    nom_com = db.Column(db.Unicode)
    syn_lieudit = db.Column(db.Unicode)


class LieuTir(serializableModel, db.Model):
    __tablename__ = 'lieu_tir'
    __table_args__ = {'schema': 'chasse'}
    id = db.Column(db.Integer, primary_key=True)
    geom = db.Column('geom', Geometry('MULTIPOLYGON', srid=2154))
    nom_lieudit = db.Column(db.Unicode)
    code_com = db.Column(db.Integer)
    nom_com = db.Column(db.Unicode)
    zon_cyneg = db.Column(db.Integer)
    zon_cyne0 = db.Column(db.Unicode)
    code_lieudit = db.Column(db.Integer)

    def as_geofeature(self):
        geometry = to_shape(self.geom)
        feature = Feature(
                id=self.id,
                geometry=geometry,
                properties={
                    c.name: getattr(self, c.name)
                    for c in self.__table__.columns if c.name != 'geom'
                }
            )
        return feature


class SaisonChasse(serializableModel, db.Model):
    __tablename__ = 'saison_chasse'
    __table_args__ = {'schema': 'chasse'}
    id = db.Column(db.Integer, primary_key=True)
    date_min = db.Column(db.DateTime)
    date_max = db.Column(db.DateTime)
    saison = db.Column(db.Unicode)
    current = db.Column(db.Boolean)
    date_debut_cerfs = db.Column(db.DateTime)
    date_fin_cerfs = db.Column(db.DateTime)
    date_debut_chevreuils = db.Column(db.DateTime)
    date_fin_chevreuils = db.Column(db.DateTime)


class PlanChasse(serializableModel, db.Model):
    __tablename__ = 'plan_chasse'
    __table_args__ = {'schema': 'chasse'}
    id = db.Column(db.Integer, primary_key=True)
    massif_affecte = db.Column(db.Unicode)
    massif_realise = db.Column(db.Unicode)
    z_i_affectee = db.Column(db.Unicode)
    z_i_realisee = db.Column(db.Unicode)
    mortalite_hors_pc = db.Column(db.Boolean)
    code_lieu_dit = db.Column(db.Unicode)
    insee = db.Column(db.Unicode)
    cd_com = db.Column(db.Integer)
    no_bracelet = db.Column(db.Unicode)
    auteur_tir = db.Column(db.Unicode)
    auteur_constat = db.Column(db.Unicode)
    date_exacte = db.Column(db.DateTime)
    sexe = db.Column(db.Unicode)
    classe_age = db.Column(db.Unicode)
    poids_entier = db.Column(db.Float)
    poids_vide = db.Column(db.Float)
    poids_c_f_p = db.Column(db.Float)
    long_dagues_droite = db.Column(db.Float)
    long_dagues_gauche = db.Column(db.Float)
    long_mandibules_droite = db.Column(db.Float)
    long_mandibules_gauche = db.Column(db.Float)
    cors_commentaire = db.Column(db.Unicode)
    cors_nb = db.Column(db.Integer)
    gestation = db.Column(db.Boolean)
    mode_chasse = db.Column(db.Unicode)
    obs = db.Column(db.Unicode)
    date_enreg = db.Column(db.DateTime)
    pk_nom_lieudit = db.Column(db.Integer)
    nom_vern = db.Column(db.Unicode)
    parc_onf = db.Column(db.Boolean)
    poids_ind = db.Column(db.Boolean)
    fk_saison = db.Column(db.Integer)
    cors_indetermine = db.Column(db.Boolean)
    long_dagues_indertermine = db.Column(db.Boolean)
    long_mandibules_indertermine = db.Column(db.Boolean)
    numerisateur = db.Column(db.Integer)
