from flask import Blueprint

categories = Blueprint('categories', __name__)


@categories.route('/', methods=['GET'])
def get_categories():
    """
    return all categories of that user
    """
    pass


@categories.route('/', methods=['POST'])
def new_category():
    """
    input: request new category
    output:
        - add the category successfully (if not existed)
        - raise error for existed category
    """
    pass

