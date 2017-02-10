#coding: utf8
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import importlib
import datetime

db = SQLAlchemy()
app_globals = {}

def init_app():
    if app_globals.get('app', False):
        app = app_globals['app']
    else :
        app = Flask(__name__)

    app.config.from_pyfile('config.py')
    db.init_app(app)

    from modules.index import routes
    app.register_blueprint(routes, url_prefix='/')


    fnauth = importlib.import_module("modules.UsersHub-authentification-module.routes")
    app.register_blueprint(fnauth.routes, url_prefix='/api/auth')

    from modules.chasse.routes import ltroutes, pcroutes
    app.register_blueprint(ltroutes, url_prefix='/api/lieux')
    app.register_blueprint(pcroutes, url_prefix='/api/plan_chasse')

    from modules.thesaurus.routes import tthroutes
    app.register_blueprint(tthroutes, url_prefix='/api/thesaurus')
    return app

if __name__ == '__main__':
    init_app().run()
