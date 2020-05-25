from flask import Blueprint, jsonify

from app import db
from app.models.categories import CategoryModel
from app.schemas.categories import CategorySchema
from app.helpers import validate_input

# create blueprint for categories
categories_blueprint = Blueprint("categories", __name__)


@categories_blueprint.route("/categories", methods=["GET"])
def get_categories():
    """
    input:
    output: return all categories in the catalog
    """

    list_categories = db.session.query(CategoryModel).all()

    return jsonify(CategorySchema(many=True).dump(list_categories)), 200


@categories_blueprint.route("/categories", methods=["POST"])
@validate_input(CategorySchema)
def create_category(data):
    """
    input: request new category (category name, description)
    output:
        - add the category successfully (if not existed) --> 200
        - raise error for existed category
    """
    name = data["name"]
    description = data["description"]

    category = db.session.query(CategoryModel).filter(CategoryModel.name == name).first()
    if category:
        return jsonify({"message": "Existed category"}), 400

    new_category = CategoryModel(name, description)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message': "Created category successfully"}), 201
