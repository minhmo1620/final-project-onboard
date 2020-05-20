import os
from app.config.base import Config


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mia@localhost/app'


