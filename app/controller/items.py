from flask import Blueprint

items = Blueprint('items', __name__)


@items.route('/', methods=['GET'])
def get_items(category_id):
	"""
	input: category id
	output: show all items in that category
	"""


@items.route('/', methods=['POST'])
def new_item(category_id, item_id):
	"""
	input: name of new item and the category
	output:
		- add new item to the category successfully
		- raise error for existed item
	"""
	pass


@items.route('/<int:item_id>', methods=['GET'])
def get_item(category_id, item_id):
	"""
	input: item
	output: item id and description
	"""
	pass


@items.route('/<int:item_id>', methods=['DELETE'])
def del_item(category_id, item_id):
	"""
	input: name of item
	output: delete from item list
	"""
	pass


@items.route('/<int:item_id>', methods=['PUT'])
def edit_item(category_id, item_id):
	"""
	input: name of item
	output: updated description
	"""
	pass
