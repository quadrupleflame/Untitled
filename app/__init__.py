import os
from flask import Flask
from flask_restful import Api
from flask import Blueprint
from flask_bootstrap import Bootstrap
# from flask_sqlalchemy import SQLAlchemy


api_bp = Blueprint('api', __name__)
api = Api(api_bp)
# db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    if not os.path.isdir(app.instance_path):
        try:
            os.mkdir(app.instance_path)
        except OSError:
            raise OSError('Cannot create instance path')
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    from . import rest
    api.add_resource(rest.Test, '/api/test/<test_val>')
    api.add_resource(rest.URLAnalysis, '/api/url')
    api.add_resource(rest.TextAnalysis, '/api/text')
    api.add_resource(rest.TextMask, '/api/mask')
    app.register_blueprint(api_bp)
    

    bootstrap = Bootstrap(app)
    return app
