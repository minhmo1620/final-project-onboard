from flask import Blueprint, jsonify

from app import db
from app.helpers import validate_input, token_required
from app.models.items import ItemModel
from app.models.categories import CategoryModel
from app.schemas.items import ItemSchema, UpdateItem

items_blueprint = Blueprint("items", __name__)


@items_blueprint.route("/categories/<int:category_id>/items", methods=["GET"])
def get_items(category_id):
    """
    input: category id (int)
    output: show all items in that category
        - each item: name of item
    """
    # check the category based on category_id
    category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404

    # query all items in that category
    list_items = db.session.query(ItemModel).filter(ItemModel.category_id == category_id).all()

    return jsonify(ItemSchema(many=True).dump(list_items)), 200


@items_blueprint.route("/categories/<int:category_id>/items", methods=["POST"])
@token_required
@validate_input(schema=ItemSchema)
def create_item(category_id, user_id, data):
    """
    input:
        - category_id (int)
        - new item information
            - item name (str)
            - item description (str)
    output:
        - add new item to the category successfully
        - raise error for existed item
    """
    # check the category based on category_id
    category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404
    name = data["name"]
    description = data["description"]

    item = db.session.query(ItemModel).filter(ItemModel.category_id == category_id)\
        .filter(ItemModel.name == name).first()

    # existing item
    if item:
        return jsonify({"message": "Existed item"}), 400

    # create a new item and save to database
    new_item = ItemModel(name=name, description=description, category_id=category_id, user_id=user_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({"message": "Created item successfully"}), 201


@items_blueprint.route("/categories/<int:category_id>/items/<int:item_id>", methods=["GET"])
def get_item(item_id, category_id):
    """
    input:
        - category_id (int)
        - item_id (int)
    output:
    - item id and description (if found)
    - return error if not
    """
    # check the category based on category_id
    category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404

    # query based on item id
    item = db.session.query(ItemModel).filter(ItemModel.category_id == category_id) \
        .filter(ItemModel.id == item_id).first()

    # check the validity
    if not item:
        return jsonify({"message": "Item not found"}), 404
    return jsonify(ItemSchema().dump(item)), 200


@items_blueprint.route("/categories/<int:category_id>/items/<int:item_id>", methods=["DELETE"])
@token_required
def delete_item(item_id, user_id, category_id):
    """
    input: item_id, category_id
    output: delete from item list
    """
    # check the category of item
    category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404

    item = db.session.query(ItemModel).filter(ItemModel.category_id == category_id) \
        .filter(ItemModel.id == item_id).first()

    # if item is in the database
    if not item:
        return jsonify({"message": "Item not found"}), 404

    # unauthorized
    if item.user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    # authorized
    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "Deleted item successfully"}), 200


@items_blueprint.route("/categories/<int:category_id>/items/<int:item_id>", methods=["PUT"])
@token_required
@validate_input(schema=UpdateItem)
def edit_item(item_id, user_id, data, category_id):
    """
    input: item_id
    output:
        - updated description (if existed)
        - raise error if not existed
    """
    # check the category of item
    category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        return jsonify({"message": "Category not found"}), 404

    # information - new description
    description = data["description"]

    # query the target item
    item = db.session.query(ItemModel).filter(ItemModel.category_id == category_id) \
        .filter(ItemModel.id == item_id).first()

    # item not found
    if not item:
        return jsonify({"message": "Item not found"}), 404

    # unauthorized
    if item.user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 403

    # authorized
    # update
    item.description = description
    db.session.commit()

    # format output
    return jsonify(ItemSchema().dump(item)), 200
