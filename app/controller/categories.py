from flask import Blueprint, request, jsonify
from ..models.categories import CategoryModel
from app import db


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
    category_name = data['name']
    category_description = data['description']

    if CategoryModel.find_by_name(category_name):
        return jsonify({'message': 'existed category'}), 400

    new_category = CategoryModel(category_name, category_description)
    new_category.save_to_db()

    return jsonify({'message': "Created item successfully"}), 201

