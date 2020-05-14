import random
import hashlib

from flask import Flask, render_template, request, redirect, url_for, session
from flask_restful import Resource
from flask_jwt import JWT

from security import authenticate, identity
from models.users import UserModel
from models.items import ItemModel
from models.categories import CategoryModel

from app import db, app

@app.route('/'):
def homepage():
	pass

@app.route('/register'):
def register():
	pass

@app.route('/login'):
def login():
	pass

@app.route('/logout'):
def logout():
	pass

@app.route('/categories', methods = ['GET'])
def get_categories():
	"""
	return all categories of that user
	"""
	pass

@app.route('/categories', methods= ['POST'])
def new_category():
	"""
	input: request new category
	ouput: 
		- add the category sucessfully (if not existed)
		- raise error for existed category
	"""
	pass

@app.route('/categories/<string:category>', methods=['GET'])
def get_category(category):
	"""
	input: name of the category
	output: all items of that category
	"""
	pass

@app.route('/categories/<string:category>/<string:item>', methods= ['POST'])
def new_item(category, item):
	"""
	input: name of new item and the category
	output:
		- add new item to the category sucessfully
		- raise error for existed item
	"""
	pass

@app.route('/categories/<string:category>/<string:item>', methods= ['GET'])
def get_item(category, item):
	"""
	input: item
	ouput: item name and description
	"""
	pass

@app.route('/categories/<string:category>/<string:item>', methods= ['DELETE'])
def del_item(category, item):
	"""
	input: name of item
	output: delete from item list
	"""
	pass

@app.route('/categories/<string:category>/<string:item>', methods = ['PUT'])
def edit_item(category, item):
	"""
	input: name of item
	output: updated description
	"""
	pass


