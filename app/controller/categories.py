from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app import db
from ..models.categories import CategoryModel, CategorySchema


categories = Blueprint('categories', __name__)


@categories.route('/categories', methods=['GET'])
def get_categories():
    """
    input:
    output: return all categories in the catalog
    """
    list_categories = db.session.query(CategoryModel)
    res = []
    for i in list_categories:
        res.append(i.name)
    return jsonify({"categories": res}), 200


@categories.route('/categories', methods=['POST'])
def create_category():
    """
    input: request new category (category name, description)
    output:
        - add the category successfully (if not existed) --> 200
        - raise error for existed category
    """
    data = request.get_json()
    try:
        result = CategorySchema().load(data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    category_name = data['name']
    category_description = data['description']

    if CategoryModel.find_by_name(category_name):
        return jsonify({'message': 'existed category'}), 400


    #new_category = result
    new_category = CategoryModel(category_name, category_description)
    new_category.save_to_db()

    return jsonify({'message': "Created item successfully"}), 201

