# coding: utf8
from flask import Blueprint, request
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select

from .models import VLieuTirSynonymes, PlanChasse, SaisonChasse
from ..utils.utilssqlalchemy import json_resp

from pypnusershub import routes as fnauth

from modules.database import DB

ltroutes = Blueprint('lieux_tir', __name__)


@ltroutes.route('/', methods=['GET'])
@ltroutes.route('/<int:id>', methods=['GET'])
@json_resp
def get_lieutirsyn(id=None):
    q = DB.session.query(VLieuTirSynonymes)

    if request.args.get('code_com'):
        q = q.filter_by(code_com=request.args.get('code_com'))

    if id:
        q = q.filter_by(id=id)

    try:
        data = q.all()
    except Exception as e:
        DB.session.rollback()
        raise
    return [attribut.as_dict() for attribut in data]


@ltroutes.route('/communes', methods=['GET'])
@json_resp
def get_communes():
    q = DB.session \
        .query(VLieuTirSynonymes.nom_com, VLieuTirSynonymes.code_com) \
        .distinct(VLieuTirSynonymes.nom_com)
    try:
        data = q.all()
    except Exception as e:
        DB.session.rollback()
        raise

    return [
        {"value": attribut.nom_com, "id": int(attribut.code_com)}
        for attribut in data
    ]


pcroutes = Blueprint('plan_chasse', __name__)


@pcroutes.route('/bracelet/<int:id>', methods=['GET'])
@fnauth.check_auth(3, False)
@json_resp
def get_bracelet_detail(id=None):
    q = DB.session.query(PlanChasse).filter_by(id=id)

    try:
        data = q.first()
    except Exception as e:
        DB.session.rollback()
        raise
    return data.as_dict()


@pcroutes.route('/bracelet/<int:id>', methods=['POST', 'PUT'])
@fnauth.check_auth(3, True)
def insertupdate_bracelet_detail(id=None, id_role=None):
    data = json.loads(request.data.decode('utf8'))
    data['numerisateur'] = id_role
    o = PlanChasse(**data)
    DB.session.merge(o)
    try:
        DB.session.commit()
        return json.dumps({
            'success': True,
            'message': 'Enregistrement sauvegardé avec succès !'
        }), 200, {'ContentType': 'application/json'}
    except Exception as e:
        DB.session.rollback()
        return json.dumps({
            'success': False,
            'message': 'Impossible de sauvegarder l\'enregistrement'
        }), 500, {'ContentType': 'application/json'}


@pcroutes.route('/auteurs', methods=['GET'])
@json_resp
def get_auteurs():

    s1 = select([PlanChasse.auteur_tir]).distinct()
    s2 = select([PlanChasse.auteur_constat]).distinct()
    q = s1.union(s2).alias('auteurs')

    try:
        data = DB.session.query(q).all()
    except Exception as e:
        DB.session.rollback()
        raise
    return [{"auteur_tir": a} for a in data]


@pcroutes.route('/saison', methods=['GET'])
@json_resp
def get_saison_list():
    q = DB.session.query(SaisonChasse)
    try:
        data = q.all()
    except Exception as e:
        DB.session.rollback()
        raise

    return [a.as_dict() for a in data]


@pcroutes.route('/bracelets_list/<int:saison>', methods=['GET'])
@json_resp
def get_bracelet_list(saison=None):
    q = DB.session \
        .query(PlanChasse.id, PlanChasse.no_bracelet) \
        .filter_by(fk_saison=saison)\
        .distinct()

    try:
        data = q.all()
    except Exception as e:
        DB.session.rollback()
        raise
    return [
        {"no_bracelet": attribut.no_bracelet, "id": int(attribut.id)}
        for attribut in data
    ]
