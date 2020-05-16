from flask import Blueprint
from flask_jwt import jwt_required

items = Blueprint('items', __name__)


@items.route('/categories/<int:category_id>/items', methods=['GET'])
def get_items(category_id):
	"""
	input: category id
	output: show all items in that category
	"""


@items.route('/categories/<int:category_id>/items', methods=['POST'])
@jwt_required()
def create_item(category_id):
	"""
	input: category_id and new item (item name, item description)
	output:
		- add new item to the category successfully
			- item_id, item_name, item_description, user_id
		- raise error for existed item
	"""
	pass


@items.route('/categories/<int:category_id>/items/<int:item_id>', methods=['GET'])
def get_item(category_id, item_id):
	"""
	input: category_id, item_id
	output: item id and description
	"""
	pass


@items.route('/categories/<int:category_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_item(category_id, item_id):
	"""
	input: item_id, category_id
	output: delete from item list
	"""
	pass


@items.route('/categories/<int:category_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required()
def edit_item(category_id, item_id):
	"""
	input: item_id
	output:
		- updated description (if existed)
		- raise error if not existed
	"""
	pass
