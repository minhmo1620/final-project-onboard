from flask import Blueprint, jsonify, request
from app import db
from app.helpers import validate_input, token_required
from app.models.items import ItemModel, ItemSchema
from app.models.categories import CategoryModel

items_blueprint = Blueprint('items', __name__)


@items_blueprint.route('/categories/<int:category_id>/items', methods=['GET'])
def get_items(category_id):
    """
    input: category id (int)
    output: show all items in that category
        - each item: name of item
    """

    # query all items in that category
    list_items = db.session.query(ItemModel).filter(ItemModel.category_id == category_id).all()

    # format output by marshmallow
    res = ItemSchema(many=True).dump(list_items)

    # category name
    category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first().name
    return jsonify({str(category): res}), 200


@items_blueprint.route('/categories/<int:category_id>/items', methods=['POST'])
@token_required
@validate_input(schema="item")
def create_item(category_id, user_id):
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
    # take response body
    data = request.get_json()

    # get item name and description from request
    item_name = data['name']
    item_description = data['description']

    # query item to check the existent of item in a specific category
    item = db.session.query(ItemModel).filter(ItemModel.category_id == category_id)\
        .filter(ItemModel.name == item_name).first()

    # existing item
    if item:
        return jsonify({'message': 'Item is existed'}), 400

    # create a new item and save to database
    new_item = ItemModel(item_name, item_description, category_id, user_id)
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'message': 'created!'}), 201


@items_blueprint.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
def get_item(item_id, **__):
    """
    input:
        - category_id (int)
        - item_id (int)
    output:
    - item id and description (if found)
    - raise error if not
    """
    # query based on item id
    item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

    # check the validity
    if not item:
        return jsonify({"message": "item not found"}), 404
    return jsonify(ItemSchema().dump(item)), 200


@items_blueprint.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(item_id, user_id, **__):
    """
    input: item_id, category_id
    output: delete from item list
    """

    # query the item based on item id
    item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

    # if item is in the database
    if not item:
        return jsonify({"message": "item not found"}), 404

    # unauthorized
    if item.user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 401

    # authorized
    db.session.delete(item)
    db.session.commit()

    return jsonify({"message": "deleted!"}), 200


@items_blueprint.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@token_required
@validate_input(schema="item")
def edit_item(item_id, user_id, **__):
    """
    input: item_id
    output:
        - updated description (if existed)
        - raise error if not existed
    """
    # take json body of request
    data = request.get_json()

    # information - new description
    description = data['description']

    # query the target item
    item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

    # item not found
    if not item:
        return jsonify({"message": "item not found"}), 404

    # unauthorized
    if item.user_id != user_id:
        return jsonify({"message": "Unauthorized"}), 401

    # authorized
    # update
    item.description = description

    # format output
    return jsonify(ItemSchema().dump(item)), 200
