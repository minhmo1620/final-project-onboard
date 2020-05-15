import os
from .local import Config

class ProductionConfig(Config):

    DB_SERVER = '192.168.19.32'