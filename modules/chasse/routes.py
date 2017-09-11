#coding: utf8
from flask import Blueprint, request
import json
from sqlalchemy import select

from server import db

from .models import VLieuTirSynonymes, PlanChasse, SaisonChasse
from ..utils.utilssqlalchemy import json_resp


ltroutes = Blueprint('lieux_tir', __name__)


@ltroutes.route('/', methods=['GET'])
@ltroutes.route('/<int:id>', methods=['GET'])
@json_resp
def get_lieutirsyn(id = None):
    q = db.session.query(VLieuTirSynonymes)

    if request.args.get('code_com') :
        print ('code_com', request.args.get('code_com'))
        q = q.filter_by(code_com = request.args.get('code_com'))

    if id:
        q = q.filter_by(id=id)

    data = q.all()
    return [attribut.as_dict() for attribut in data]


@ltroutes.route('/communes', methods=['GET'])
@json_resp
def get_communes():
    data = db.session \
        .query(VLieuTirSynonymes.nom_com, VLieuTirSynonymes.code_com) \
        .distinct(VLieuTirSynonymes.nom_com).all()
    return  [{"value" : attribut.nom_com, "id" : int(attribut.code_com) } for attribut in data]

pcroutes = Blueprint('plan_chasse', __name__)

@pcroutes.route('/bracelet/<int:id>', methods=['GET'])
@json_resp
def get_bracelet_detail(id = None):
    data = db.session.query(PlanChasse).filter_by(id=id).first()
    return data.as_dict()

@pcroutes.route('/bracelet/<int:id>', methods=['POST', 'PUT'])
def insertupdate_bracelet_detail(id = None):
    data = json.loads(request.data)
    o = PlanChasse(**data)
    db.session.merge(o)
    try:
        db.session.commit()
        return json.dumps({'success':True, 'message':'Enregistrement sauvegardé avec success'}), 200, {'ContentType':'application/json'}
    except Exception as e:
        db.session.rollback()
        return json.dumps({'success':False, 'message':'Impossible de sauvegarder l\'enregistrement'}), 500, {'ContentType':'application/json'}

@pcroutes.route('/auteurs', methods=['GET'])
@json_resp
def get_auteurs():

    s1 = select([PlanChasse.auteur_tir]).distinct()
    s2 = select([PlanChasse.auteur_constat]).distinct()
    q = s1.union(s2).alias('auteurs')
    data = db.session.query(q).all()
    return [{"auteur_tir" : a }for a in data]

@pcroutes.route('/saison', methods=['GET'])
@json_resp
def get_saison_list():
    data = db.session.query(SaisonChasse).all()
    return [a.as_dict() for a in data]

@pcroutes.route('/bracelets_list/<int:saison>', methods=['GET'])
@json_resp
def get_bracelet_list(saison = None):
    data = db.session \
        .query(PlanChasse.id, PlanChasse.no_bracelet) \
        .filter_by(fk_saison = saison)\
        .distinct().all()
    return  [{"no_bracelet" : attribut.no_bracelet, "id" : int(attribut.id) } for attribut in data]
