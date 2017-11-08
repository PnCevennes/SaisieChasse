# coding: utf8
from flask import Blueprint, request
from flask_sqlalchemy import SQLAlchemy

from .models import Thesaurus
from ..utils.utilssqlalchemy import json_resp

db = SQLAlchemy()
tthroutes = Blueprint('thesaurus', __name__)


@tthroutes.route('/vocabulary/<int:id>', methods=['GET'])
@json_resp
def get_vocabulary(id=None):
    q = db.session.query(
            Thesaurus.id,
            Thesaurus.code,
            Thesaurus.libelle,
            Thesaurus.hierarchie
        ).filter(Thesaurus.id_type == id, Thesaurus.fk_parent != 0)

    params = request.args
    if params.get('ilikeHierachie'):
        q = q.filter(Thesaurus.hierarchie.like(params.get('ilikeHierachie')))

    try:
        data = q.all()
    except Exception as e:
        db.session.rollback()
        raise

    return [
        {
            "id": a.id,
            "code": a.code,
            "libelle": a.libelle,
            "hierarchie": a.hierarchie
        }
        for a in data
    ]
