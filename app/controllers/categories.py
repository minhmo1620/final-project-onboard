from flask import Blueprint, request, jsonify

from app import db
from app.models.categories import CategoryModel, CategorySchema
from app.helpers import validate_input

# create blueprint for categories
categories = Blueprint('categories', __name__)


@categories.route('/categories', methods=['GET'])
def get_categories():
    """
    input:
    output: return all categories in the catalog
    """
    # query
    list_categories = db.session.query(CategoryModel).all()

    res = CategorySchema(many=True).dump(list_categories)

    return jsonify({"categories": res}), 200


@categories.route('/categories', methods=['POST'])
@validate_input("category")
def create_category():
    """
    input: request new category (category name, description)
    output:
        - add the category successfully (if not existed) --> 200
        - raise error for existed category
    """
    # take the input
    data = request.get_json()

    # information - name & description
    category_name = data['name']
    category_description = data['description']

    # check the existent of item
    if CategoryModel.find_by_name(category_name):
        return jsonify({'message': 'existed category'}), 400

    # create a new category and add to database
    new_category = CategoryModel(category_name, category_description)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message': "Created item successfully"}), 201
