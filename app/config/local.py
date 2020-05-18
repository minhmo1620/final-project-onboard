import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mia@localhost/app'