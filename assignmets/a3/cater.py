# -*- coding: utf-8 -*-
"""
	Cater app
"""

import time
import os
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

from models import db, User, Event, Event_Assignee
# from modle import db

# create our little application :)
app = Flask(__name__)

# configuration
DEBUG = True
SECRET_KEY = 'secret_key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.root_path, 'cater.db')

app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

db.init_app(app)


class Event_Stuff:
	e = Event(datetime.now(), 0)
	stuff = []
 	
	def __init__(self, e,stuff):
		self.e= e
		self.stuff = stuff
		
		
@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	db.create_all()
	# add the owner 
	db.session.add(User('owner', 'owner', generate_password_hash('pass')))
	db.session.commit()
	#add stuff for debug
	db.session.add(User('stuff', 'stuff', generate_password_hash('pass')))
	db.session.commit()
	
	print('Initialized the database.')
 
 	
def get_user_id(username):
	"""Convenience method to look up the id for a username."""
	rv = User.query.filter_by(username=username).first()
	return rv.user_id if rv else None
 
 
def format_datetime(timestamp):
	"""Format a timestamp for display."""
	return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')
 
 
@app.before_request
def before_request():
	g.user = None
	if 'user_id' in session:
		g.user = User.query.filter_by(user_id=session['user_id']).first()
 
@app.route('/')
def main_page():
	"""Shows a users timeline or if no user is logged in it will
	redirect to the login timeline.  This timeline shows the user's
	messages as well as all the messages of followed users.
	"""
	if not g.user:
		return redirect(url_for('login'))
 
	u = User.query.filter_by(user_id=session['user_id']).first()
	return redirect(url_for('user'))

@app.route('/user')
def user():
	"""All signed users are directed here and then according to thier title will
	   be redirected to other routes"""
	if not g.user:
		return redirect(url_for('login'))
	u = User.query.filter_by(user_id=session['user_id']).one()
	if u.title == "customer":
		return redirect(url_for('customer_event'))
	if u.title == "stuff":
		return redirect(url_for('stuff'))
	if u.title == "owner":
		return redirect(url_for('owner'))


@app.route('/customer_event', methods=['GET', 'POST'])
def customer_event():
	"""Customer event and adding a new event form"""
	if not g.user:
		return redirect(url_for('login'))
	
	'''Remove an event from the datebase'''
	rm_event_id = request.args.get('rm_event_id')
	if rm_event_id:
		if Event.query.filter(Event.event_id==rm_event_id):
			Event.query.filter(Event.event_id==rm_event_id).delete()
			db.session.commit()
			flash('You have removed an event')
			return redirect(request.path,code=302)

	
	events = Event.query.filter_by(booked_by_user_id=session['user_id']).all()
	error = None
	if request.method == 'POST':
		if not request.form['date']:
			error = 'You have to enter a date'
		else:
			events = Event.query.all()
			isDateBusy=False
			for event in events:
				if event.date == datetime.strptime(request.form['date'], '%Y-%m-%d').date():
					isDateBusy = True
			if isDateBusy:
# 				flash('Chose a different day, this day is already booked')
				error = 'Chose a different day, this day is already booked'
			else:	
				db.session.add(Event(datetime.strptime(request.form['date'], '%Y-%m-%d'), session['user_id'] ))
				db.session.commit()
				flash('You have created a new event')
# 			flash(Event.query.filter_by(booked_by_user_id=session['user_id']).all())
# 			flash(isDateBusy)
			events = Event.query.filter_by(booked_by_user_id=session['user_id']).all()
			return render_template('customer_event.html',error=error, events=events)
	return render_template('customer_event.html', error=error, events=events)

@app.route('/stuff', methods=['GET', 'POST'])
def stuff():
	"""stuff dashboar."""
	if not g.user:
		return redirect(url_for('login'))
	error = None
	
	events = Event.query.all()
	events_tmp = events[:]
	events = []	
	
	'''remove already signedup events'''
	event_a = Event_Assignee.query.\
						filter(Event_Assignee.user_id==session['user_id']).all();
	all_signed_ids = []
	for e in event_a:
		all_signed_ids .append(e.event_id)
	
	
	'''remove more than 3 assigned events'''
	sql = '''select event_id, count(*) as count 
			from event__assignee  
			group by event_id'''
	result = db.engine.execute(sql)
	all_biger3_ids = []
	for row in result:
		if row[1] >= 3:
			all_biger3_ids.append(row[0]) 
			
	for e in events_tmp:
		if e.event_id not in all_biger3_ids and e.event_id not in all_signed_ids:
			events.append(e)
	
	
	'''Get all signed events for current user'''			
	event_a = Event_Assignee.query.filter(Event_Assignee.user_id == session['user_id']).all()
	all_event_ids = []
	for e in event_a:
		all_event_ids.append(e.event_id)
	event_a = Event.query.all()
	cur_events =[]
	for e in event_a:
		if e.event_id in all_event_ids:
			cur_events.append(e) 
	event_a = cur_events

	'''Assign for a new event'''
	sign_event_id = request.args.get('sign_event_id')
	if sign_event_id:
		
		
		'''Assign a stuff to this event'''
		db.session.add(Event_Assignee(sign_event_id, session['user_id']))
		db.session.commit();
		flash('You have signed to an event');
		return redirect(request.path,code=302)
 
 										  
	return render_template('stuff.html', error=error, events=events, signed_events=event_a )
 


@app.route('/owner')
def owner():
	"""owner dashboar."""
	if not g.user:
		return redirect(url_for('login'))
	error = None
	events_s = []
	# Get all the Events 
	events = Event.query.all()	
	# Get assigned stuff for each event 
	for e in events:
		stuff  = []
		sql = """
			select * 
			from user  
			inner join event__assignee on user.user_id=event__assignee.user_id
			where event__assignee.event_id ="""
		sql += str(e.event_id)
 			
		result = db.engine.execute(sql)
		for row in result:
			u = User.query.filter(User.user_id == row[0]).one()
			stuff.append(u)
		events_s.append(Event_Stuff(e,stuff))

	return render_template('owner.html', error=error, events_stuff = events_s )

 
@app.route('/create_new_stuff', methods=['GET', 'POST'])
def create_new_stuff():
	if not g.user:
		return redirect(url_for('login'))
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif get_user_id(request.form['username']) is not None:
			error = 'The username is already taken'
		else:
			db.session.add(User(request.form['username'], "stuff", generate_password_hash(request.form['password'])))
			db.session.commit()
			flash('You were successfully create a new account')
			return redirect(url_for('owner'))
	return render_template('create_new_stuff.html', error=error)
	

@app.route('/login', methods=['GET', 'POST'])
def login():
	"""Logs the user in."""
	if g.user:
		return redirect(url_for('main_page'))
	error = None
	if request.method == 'POST':
 
		user = User.query.filter_by(username=request.form['username']).first()
		if user is None:
			error = 'Invalid username'
		elif not check_password_hash(user.pw_hash, request.form['password']):
			error = 'Invalid password'
		else:
			flash('You were logged in')
			session['user_id'] = user.user_id
			return redirect(url_for('main_page'))
	return render_template('login.html', error=error)
 

@app.route('/register', methods=['GET', 'POST'])
def register():
	"""Registers the user."""
	if g.user:
		return redirect(url_for('login'))
	error = None
	if request.method == 'POST':
		if not request.form['username']:
			error = 'You have to enter a username'
		elif not request.form['password']:
			error = 'You have to enter a password'
		elif request.form['password'] != request.form['password2']:
			error = 'The two passwords do not match'
		elif get_user_id(request.form['username']) is not None:
			error = 'The username is already taken'
		else:
			db.session.add(User(request.form['username'], "customer", generate_password_hash(request.form['password'])))
			db.session.commit()
			flash('You were successfully registered and can login now')
			return redirect(url_for('login'))
	return render_template('register.html', error=error)
 
 
@app.route('/logout')
def logout():
	"""Logs the user out."""
	flash('You were logged out')
	session.pop('user_id', None)
	return redirect(url_for('login'))
 
 
# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime

