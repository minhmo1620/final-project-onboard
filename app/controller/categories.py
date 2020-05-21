from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app import db
from app.models.categories import CategoryModel, CategorySchema

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

    # format by marshmallow
    res = [CategorySchema().dump(i) for i in list_categories]

    return jsonify({"categories": res}), 200


@categories.route('/categories', methods=['POST'])
def create_category():
    """
    input: request new category (category name, description)
    output:
        - add the category successfully (if not existed) --> 200
        - raise error for existed category
    """
    # take the input
    data = request.get_json()

    # check the validity of the input
    try:
        CategorySchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    # information - name & description
    category_name = data['name']
    category_description = data['description']

    # check the existent of item
    if CategoryModel.find_by_name(category_name):
        return jsonify({'message': 'existed category'}), 400

    # create a new category and add to database
    new_category = CategoryModel(category_name, category_description)
    new_category.save_to_db()

    return jsonify({'message': "Created item successfully"}), 201
