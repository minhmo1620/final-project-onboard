from flask import Blueprint

categories = Blueprint('categories', __name__)


@categories.route('/categories', methods=['GET'])
def get_categories():
    """
    input:
    output: return all categories in the catalog
    """
    pass


@categories.route('/categories', methods=['POST'])
def create_category():
    """
    input: request new category (category name, description)
    output:
        - add the category successfully (if not existed) --> 200
        - raise error for existed category
    """
    pass

