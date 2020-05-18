import os
from app.config.local import Config


# class DevelopmentConfig(Config):
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mia@localhost/app'
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False


