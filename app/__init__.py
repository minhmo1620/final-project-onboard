import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .db import db
from .models.users import UserModel
from .models.items import ItemModel
from .models.categories import CategoryModel

ENV_TO_CONFIG = {'test': 'app.configs.test.TestingConfig',
                 'development': 'app.configs.development.DevelopmentConfig',
                 'local': 'app.configs.local.LocalConfig',
                 'production': 'app.configs.production.ProductionConfig'}


def create_app(env):
    app = Flask(__name__)
    app.config.from_object(ENV_TO_CONFIG[env])
    db.init_app(app)

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify({"message": str(e)}), code

    with app.app_context():
        from .controllers.items import items_blueprint
        from .controllers.categories import categories_blueprint
        from .controllers.users import users_blueprint

        app.register_blueprint(categories_blueprint, url_prefix="/")
        app.register_blueprint(items_blueprint, url_prefix="/")
        app.register_blueprint(users_blueprint, url_prefix="/")

        db.create_all()

    return app


env = os.environ.get('ENV', 'development')
app = create_app(env)
# app.app_context().push()
