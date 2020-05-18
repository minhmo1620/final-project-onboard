import os
from .local import Config

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mia@localhost/app'