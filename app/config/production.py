import os
from .local import Config

class ProductionConfig(Config):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mia@localhost/app'