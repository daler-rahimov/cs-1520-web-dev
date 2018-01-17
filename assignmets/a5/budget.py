# -*- coding: utf-8 -*-
"""
	Chat app 
	Sutdent : Daler Rahimov 
	pitt id: dar158
	
"""
from __future__ import print_function
from models import Category, Purchase 
import sys
import os
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from flask import Flask, jsonify, abort, request, url_for
from flask_restful import Api
from flask_restful import Resource, fields, reqparse, marshal_with, abort
from flask import request

import datetime
import time
import email.utils

app = Flask(__name__)
api = Api(app)
app.config.update(dict(SEND_FILE_MAX_AGE_DEFAULT=0))


# configuration
DEBUG = True
app.config.from_object(__name__)
app.config.from_envvar('CHAT_CONFIG', silent=True)

# global vars 
allCats = []
allPurcheses = [] 

# debug 
c = Category("test",100,100)
allCats.append(c)
c = Category("Uncategorized",0,0,-1)
allCats.append(c)
p = Purchase(55, "shoose",datetime.datetime.now())
allPurcheses.append(p)

############################################
# Routes 
############################################
@app.route('/')
def main_page():
	""" This is the seleton page 
	"""
	return redirect(url_for('budget'))

@app.route('/budget')
def budget():
	return render_template('budget.html')
 	
 	
# add some filters to jinja
# app.jinja_env.filters['datetimeformat'] = format_datetime



 ########################################
 # API Resources 
 ########################################

cat_fields = {
	'cat_id': fields.Integer,
	'name': fields.String,
	'limit': fields.Integer,
	'spent': fields.Integer
}



cat_parser = reqparse.RequestParser(bundle_errors=True)
cat_parser.add_argument('cat_id', type=int, location='json')
cat_parser.add_argument('name', type=str, location='json')
cat_parser.add_argument('limit', type=int, location='json')
cat_parser.add_argument('spent', type=int, location='json')

class CatResource(Resource):

	@marshal_with(cat_fields)
	def delete(self, id):
		for c in allCats:
			if (c.cat_id == id):
				allCats.remove(c)
				return {}, 204	
		abort(405, message = "Category {} doesn't exitst".format(id))
		


api.add_resource(CatResource, '/cats/<int:id>', endpoint='cat')

        
class CatListResource(Resource):
	@marshal_with(cat_fields)
	def get(self):
		return allCats
	
	@marshal_with(cat_fields)
	def post(self):
		cat_arg = cat_parser.parse_args()
		c  = Category(name=cat_arg["name"], limit= cat_arg["limit"],spent=cat_arg["spent"])
		print(cat_arg["name"], file = sys.stderr)
		allCats.append(c)
		return c, 201

api.add_resource(CatListResource, '/cats/', endpoint='cats')

purch_fields = {
	'p_id': fields.Integer,
	'amount': fields.Integer,
	'spentOn': fields.String,
	'date': fields.String,
	'cat_id': fields.Integer
}

purch_parser = reqparse.RequestParser(bundle_errors=True)
purch_parser.add_argument('p_id', type=int, location='json')
purch_parser.add_argument('amount', type=int,required=True, location='json')
purch_parser.add_argument('spentOn', type=str, location='json')
purch_parser.add_argument('date', type=str, location='json')
purch_parser.add_argument('cat_id', type=int, location='json')

class PurchaseListResource(Resource):
	@marshal_with(purch_fields)
	def get(self):
		return allPurcheses
	
	@marshal_with(purch_fields)
	def post(self):
		purch_arg = purch_parser.parse_args()
		d =  datetime.datetime.fromtimestamp(time.mktime(email.utils.parsedate(purch_arg["date"])))
		p  = Purchase(purch_arg["amount"],purch_arg["spentOn"],d, purch_arg["cat_id"])
		print(purch_arg["amount"], file = sys.stderr)
		for c in allCats:
			if(c.cat_id==purch_arg["cat_id"]):
				c.spent = c.spent+purch_arg["amount"]
		allPurcheses.append(p)
		return p, 201

api.add_resource(PurchaseListResource, '/purchs/', endpoint='purchs')

