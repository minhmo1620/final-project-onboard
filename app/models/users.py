from ..db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(100))
    salt = db.Column(db.String(16))

    def __init__(self, username, password, salt):
        self.username = username
        self.password = password
        self.salt = salt
