#coding: utf8
from flask import Blueprint, request
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, distinct

from .models import VLieuTirSynonymes, PlanChasse, SaisonChasse
from ..utils.utilssqlalchemy import json_resp, GenericTable, serializeQuery, serializeQueryOneResult

from pypnusershub import routes as fnauth

db = SQLAlchemy()
realroutes = Blueprint('realisation', __name__)


@realroutes.route('/nomvern_massif', methods=['GET'])
@json_resp
def getNomVernMassif():
    tableBilanAttributionMassif = GenericTable('chasse.v_rapport_bilan_attribution_massif', 'chasse')
    col = tableBilanAttributionMassif.tableDef.columns
    q = db.session.query(col.nom_vern,col.massif).distinct()
    results = q.all()
    data = {}
    for d in db.session.query(col.nom_vern,col.massif).distinct():
        try:
            data[d.nom_vern]
        except:
            data[d.nom_vern] = []
        data[d.nom_vern].append(d.massif)
    return data


@realroutes.route('/attribution_massif', methods=['GET'])
@json_resp
def getBilanAttributionMassif():
    tableBilanAttributionMassif = GenericTable('chasse.v_rapport_bilan_attribution_massif', 'chasse')
    q = db.session.query(tableBilanAttributionMassif.tableDef)
    results = q.filter(getattr(tableBilanAttributionMassif.tableDef.columns,'nom_vern') == request.args.get('nom_vern'))\
        .filter(getattr(tableBilanAttributionMassif.tableDef.columns,'massif') ==request.args.get('massif'))\
        .all()
    return serializeQuery(results,q.column_descriptions)
