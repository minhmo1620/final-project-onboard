import os
from flask import Flask

from .db import db
from .models.users import UserModel
from .models.items import ItemModel
from .models.categories import CategoryModel


def create_app(env):
    env_list = {'test': 'app.config.staging.TestingConfig',
                'development': 'app.config.development.DevelopmentConfig',
                'local': 'app.config.local.LocalConfig',
                'production': 'app.config.production.ProductionConfig'}

    app = Flask(__name__)
    app.config.from_object(env_list[env])
    db.init_app(app)

    with app.app_context():
        from .controller.items import items
        from .controller.categories import categories
        from .controller.users import users

        app.register_blueprint(categories, url_prefix="/")
        app.register_blueprint(items, url_prefix="/")
        app.register_blueprint(users, url_prefix="/")

        db.create_all()

    return app


env = os.environ.get('ENV', 'development')
app = create_app(env)
app.app_context().push()
