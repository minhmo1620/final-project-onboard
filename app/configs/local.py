from app.configs.base import Config


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:mia@localhost/app"
