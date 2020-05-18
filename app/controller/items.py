from flask import Blueprint, jsonify, request
from flask_jwt import jwt_required
from app import db
from ..models.items import ItemModel

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
		res.append(i.json())
	return jsonify({"categories": res})


@items.route('/categories/<int:category_id>/items', methods=['POST'])
# @jwt_required()
def create_item(category_id):
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

	item_name = data['name']
	item_description = data['description']
	category_id = data['category_id']

	item = db.session.query(ItemModel).filter(ItemModel.category_id == category_id)\
		.filter(ItemModel.name == item_name).first()

	if item:
		return jsonify({'message':'existed item'})

	new_item = ItemModel(item_name, item_description, category_id)
	new_item.save_to_db()

	return jsonify({'message':'created!'})

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
	data = request.get_json()

	item_id = data['item_id']

	item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

	if item:
		return jsonify({"item": item.name, "description": item.description})
	else:
		return jsonify({"message":"item not found"})


@items.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
# @jwt_required()
def delete_item(category_id, item_id):
	"""
	input: item_id, category_id
	output: delete from item list
	"""
	data = request.get_json()

	item_id = data['item_id']

	item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

	if item:
		item.delete_from_db()
		return jsonify({"message": "deleted!"})
	else:
		return jsonify({"message": "item not found"})


@items.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
# @jwt_required()
def edit_item(category_id, item_id):
	"""
	input: item_id
	output:
		- updated description (if existed)
		- raise error if not existed
	"""
	data = request.get_json()

	item_id = data['item_id']
	description = data['description']

	item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

	if item:
		item.description = description
		return jsonify({"message": "updated!"})
	else:
		return jsonify({"message": "item not found"})
