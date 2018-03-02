# coding: utf8
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Sequence
from ..utils.genericmodels import serializableModel
from geoalchemy2 import Geometry

from modules.database import DB


class LieuTirSynonymes(serializableModel, DB.Model):
    __tablename__ = 'lieu_tir_synonymes'
    __table_args__ = {'schema': 'chasse'}
    id = DB.Column(DB.Integer, primary_key=True)
    code_lieudit = DB.Column(
        DB.Integer,
        ForeignKey("chasse.lieux_tir.code_lieudit"),
        nullable=False
    )
    libelle_lieudit = DB.Column(DB.Unicode)


class VLieuTirSynonymes(serializableModel, DB.Model):
    __tablename__ = 'v_lieu_dit_synonymes'
    __table_args__ = {'schema': 'chasse'}
    id = DB.Column(DB.Integer, primary_key=True)
    code_lieudit = DB.Column(DB.Integer)
    nom_lieudit = DB.Column(DB.Unicode)
    synonyme = DB.Column(DB.Unicode)
    code_com = DB.Column(DB.Integer)
    nom_com = DB.Column(DB.Unicode)
    syn_lieudit = DB.Column(DB.Unicode)


class LieuTir(serializableModel, DB.Model):
    __tablename__ = 'lieu_tir'
    __table_args__ = {'schema': 'chasse'}
    id = DB.Column(DB.Integer, primary_key=True)
    geom = DB.Column('geom', Geometry('MULTIPOLYGON', srid=2154))
    nom_lieudit = DB.Column(DB.Unicode)
    code_com = DB.Column(DB.Integer)
    nom_com = DB.Column(DB.Unicode)
    zon_cyneg = DB.Column(DB.Integer)
    zon_cyne0 = DB.Column(DB.Unicode)
    code_lieudit = DB.Column(DB.Integer)

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


class SaisonChasse(serializableModel, DB.Model):
    __tablename__ = 'saison_chasse'
    __table_args__ = {'schema': 'chasse'}
    id = DB.Column(DB.Integer, primary_key=True)
    date_min = DB.Column(DB.DateTime)
    date_max = DB.Column(DB.DateTime)
    saison = DB.Column(DB.Unicode)
    current = DB.Column(DB.Boolean)
    date_debut_cerfs = DB.Column(DB.DateTime)
    date_fin_cerfs = DB.Column(DB.DateTime)
    date_debut_chevreuils = DB.Column(DB.DateTime)
    date_fin_chevreuils = DB.Column(DB.DateTime)


class PlanChasse(serializableModel, DB.Model):
    __tablename__ = 'plan_chasse'
    __table_args__ = {'schema': 'chasse'}
    id = DB.Column(DB.Integer, primary_key=True)
    massif_affecte = DB.Column(DB.Unicode)
    massif_realise = DB.Column(DB.Unicode)
    z_i_affectee = DB.Column(DB.Unicode)
    z_i_realisee = DB.Column(DB.Unicode)
    mortalite_hors_pc = DB.Column(DB.Boolean)
    code_lieu_dit = DB.Column(DB.Unicode)
    insee = DB.Column(DB.Unicode)
    cd_com = DB.Column(DB.Integer)
    no_bracelet = DB.Column(DB.Unicode)
    auteur_tir = DB.Column(DB.Unicode)
    auteur_constat = DB.Column(DB.Unicode)
    date_exacte = DB.Column(DB.DateTime)
    sexe = DB.Column(DB.Unicode)
    classe_age = DB.Column(DB.Unicode)
    poids_entier = DB.Column(DB.Float)
    poids_vide = DB.Column(DB.Float)
    poids_c_f_p = DB.Column(DB.Float)
    long_dagues_droite = DB.Column(DB.Float)
    long_dagues_gauche = DB.Column(DB.Float)
    long_mandibules_droite = DB.Column(DB.Float)
    long_mandibules_gauche = DB.Column(DB.Float)
    cors_commentaire = DB.Column(DB.Unicode)
    cors_nb = DB.Column(DB.Integer)
    gestation = DB.Column(DB.Boolean)
    mode_chasse = DB.Column(DB.Unicode)
    obs = DB.Column(DB.Unicode)
    date_enreg = DB.Column(DB.DateTime)
    pk_nom_lieudit = DB.Column(DB.Integer)
    nom_vern = DB.Column(DB.Unicode)
    parc_onf = DB.Column(DB.Boolean)
    poids_ind = DB.Column(DB.Boolean)
    fk_saison = DB.Column(DB.Integer)
    cors_indetermine = DB.Column(DB.Boolean)
    long_dagues_indertermine = DB.Column(DB.Boolean)
    long_mandibules_indertermine = DB.Column(DB.Boolean)
    numerisateur = DB.Column(DB.Integer)
