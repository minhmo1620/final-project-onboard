import os
from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from .db import db
from .models.users import UserModel
from .models.items import ItemModel
from .models.categories import CategoryModel


def create_app(env):
    env_list = {'test': 'app.configs.staging.TestingConfig',
                'development': 'app.configs.development.DevelopmentConfig',
                'local': 'app.configs.local.LocalConfig',
                'production': 'app.configs.production.ProductionConfig'}

    app = Flask(__name__)
    app.config.from_object(env_list[env])
    db.init_app(app)

    @app.errorhandler(Exception)
    def handle_error(e):
        code = 500
        if isinstance(e, HTTPException):
            code = e.code
        return jsonify({"message": str(e)}), code

    with app.app_context():
        from .controllers.items import items
        from .controllers.categories import categories
        from .controllers.users import users

        app.register_blueprint(categories, url_prefix="/")
        app.register_blueprint(items, url_prefix="/")
        app.register_blueprint(users, url_prefix="/")

        db.create_all()

    return app


env = os.environ.get('ENV', 'development')
app = create_app(env)
app.app_context().push()
