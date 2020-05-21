from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from app import db

from ..models.items import ItemModel, ItemSchema
from ..models.categories import CategoryModel
from .users import token_required

items = Blueprint('items', __name__)


@items.route('/categories/<int:category_id>/items', methods=['GET'])
def get_items(category_id):
	"""
	input: category id (int)
	output: show all items in that category
		- each item: name of item
	"""

	# query all items in that category
	list_items = db.session.query(ItemModel).filter(ItemModel.category_id == category_id).all()

	# format output by marshmallow
	res = [ItemSchema().dump(i) for i in list_items]

	# category name
	category = db.session.query(CategoryModel).filter(CategoryModel.id == category_id).first().name
	return jsonify({str(category): res}), 200


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
	# take response body
	data = request.get_json()

	# check the validity of input
	try:
		ItemSchema().load(data)
	except ValidationError as err:
		return jsonify(err.messages), 422

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
	# query based on item id
	item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

	# check the validity
	if item:
		return jsonify(ItemSchema().dump(item)), 200
	else:
		return jsonify({"message": "item not found"}), 404


@items.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@token_required
def delete_item(category_id, item_id, user_id):
	"""
	input: item_id, category_id
	output: delete from item list
	"""

	# query the item based on item id
	item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

	# if item is in the database
	if item:

		# authorized
		if item.user_id == user_id:

			# delete item from db
			item.delete_from_db()
			return jsonify({"message": "deleted!"}), 200

		# unauthorized
		else:
			return jsonify({"message": "Unauthorized"}), 401

	# item not found
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
	# take json body of request
	data = request.get_json()

	# check the validity of input
	try:
		ItemSchema().load(data)
	except ValidationError as err:
		return jsonify(err.messages), 422

	# information - new description
	description = data['description']

	# query the target item
	item = db.session.query(ItemModel).filter(ItemModel.id == item_id).first()

	# if found item
	if item:

		# authorized
		if item.user_id == user_id:

			# update
			item.description = description

			# format output
			return jsonify(ItemSchema().dump(item)), 200

		# unauthorized
		else:
			return jsonify({"message": "Unauthorized"}), 401

	# item not found
	else:
		return jsonify({"message": "item not found"}), 404
