# coding: utf8
from flask import Blueprint, request
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, distinct

from .models import VLieuTirSynonymes, PlanChasse, SaisonChasse
from ..utils.utilssqlalchemy import json_resp, GenericTable, serializeQuery, serializeQueryOneResult


from pypnusershub import routes as fnauth

from . import db
realroutes = Blueprint('realisation', __name__)


@realroutes.route('/nomvern_massif', methods=['GET'])
@json_resp
def getNomVernMassif():
    tableBilanAttributionMassif = GenericTable(
        'chasse.v_rapport_bilan_attribution_massif',
        'chasse'
    )
    col = tableBilanAttributionMassif.tableDef.columns
    q = db.session.query(col.nom_vern, col.massif).distinct()
    try:
        results = q.all()
    except Exception as e:
        db.session.rollback()
        raise
    data = {}
    for d in db.session.query(col.nom_vern, col.massif).distinct():
        try:
            data[d.nom_vern]
        except Exception as e:
            data[d.nom_vern] = []
        data[d.nom_vern].append(d.massif)
    return data


@realroutes.route('/attribution_massif', methods=['GET'])
@json_resp
def getBilanAttributionMassif():
    tBAttMassif = GenericTable(
        'chasse.v_rapport_bilan_attribution_massif',
        'chasse'
    )
    tcols = tBAttMassif.tableDef.columns
    q = db.session.query(tBAttMassif.tableDef)
    try:
        results = q.filter(
            getattr(tcols, 'nom_vern') == request.args.get('nom_vern'))\
            .filter(getattr(tcols, 'massif') == request.args.get('massif'))\
            .all()
    except Exception as e:
        db.session.rollback()
        raise
    return serializeQuery(results, q.column_descriptions)
