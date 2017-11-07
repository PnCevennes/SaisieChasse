# coding: utf8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import importlib

db = SQLAlchemy()
app_globals = {}


def get_app():
    if app_globals.get('app', False):
        app = app_globals['app']
    else:
        app = Flask(__name__)

    app.config.from_pyfile('config.py')
    db.init_app(app)

    from modules.index import routes
    app.register_blueprint(routes, url_prefix='/')

    from pypnusershub import routes
    app.register_blueprint(routes.routes, url_prefix='/api/auth')

    from modules.chasse.routes import ltroutes, pcroutes
    app.register_blueprint(ltroutes, url_prefix='/api/lieux')
    app.register_blueprint(pcroutes, url_prefix='/api/plan_chasse')

    from modules.thesaurus.routes import tthroutes
    app.register_blueprint(tthroutes, url_prefix='/api/thesaurus')

    from modules.chasse.routesrealisation import realroutes
    app.register_blueprint(realroutes, url_prefix='/api/bilan')

    return app


app = get_app()

if __name__ == '__main__':
    from flask.ext.script import Manager
    Manager(app).run()
