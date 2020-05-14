from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix="")

@auth.route('/register')
def register():
    pass


@auth.route('/login')
def login():
    pass


@auth.route('/logout')
def logout():
    pass
