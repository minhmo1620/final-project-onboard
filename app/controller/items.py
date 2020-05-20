from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db
from ..models.items import ItemModel, ItemSchema
from .users import token_required

items = Blueprint('items', __name__)


@items.route('/categories/<int:category_id>/items', methods=['GET'])
def get_items(category_id):
	"""
	input: category id (int)
	output: show all items in that category
		- each item: name of item
	"""
	list_items = db.session.query(ItemModel).filter(ItemModel.category_id == category_id)
	res = []
	for i in list_items:
		res.append(i.name)
	return jsonify({"categories": res}), 200


@items.route('/categories/<int:category_id>/items', methods=['POST'])
@token_required
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
	data = request.get_json()

	try:
		res = ItemSchema().load(data)
	except ValidationError as err:
		return jsonify(err.messages), 422

	item_name = data['name']
	item_description = data['description']

	item = db.session.query(ItemModel).filter(ItemModel.category_id == category_id)\
		.filter(ItemModel.name == item_name).first()

	if item:
		return jsonify({'message': 'existed item'}), 400

	new_item = ItemModel(item_name, item_description, category_id, user_id)
	new_item.save_to_db()

	return jsonify({'message': 'created!'}), 201


@items.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
def get_item(category_id, item_id):
	"""
	input:
		- category_id (int)
		- item_id (int)
	output:
	- item id and description (if found)
	- raise error if not
	"""
	item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

	if item:
		return jsonify({"item": item.name, "description": item.description}), 200
	else:
		return jsonify({"message": "item not found"}), 404


@items.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(category_id, item_id, user_id):
	"""
	input: item_id, category_id
	output: delete from item list
	"""
	item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

	if item:
		if item.user_id == user_id:
			item.delete_from_db()
			return jsonify({"message": "deleted!"}), 200
		else:
			return jsonify({"message": "Unauthorized"}), 401
	else:
		return jsonify({"message": "item not found"}), 404


@items.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@token_required
def edit_item(category_id, item_id, user_id):
	"""
	input: item_id
	output:
		- updated description (if existed)
		- raise error if not existed
	"""
	data = request.get_json()

	try:
		ItemSchema().load(data)
	except ValidationError as err:
		return jsonify(err.messages), 422

	description = data['description']

	item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

	if item:
		if item.user_id == user_id:
			item.description = description
			return jsonify({"message": "updated!"}), 200
		else:
			return jsonify({"message": "Unauthorized"}), 401
	else:
		return jsonify({"message": "item not found"}), 404
