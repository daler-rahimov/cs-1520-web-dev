
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import date
db = SQLAlchemy()

class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(24), nullable=False)
	title = db.Column(db.String(80), nullable=False)
	pw_hash = db.Column(db.String(64), nullable=False)

# 	messages = db.relationship('Message', backref='author')
# 

 	
	def __init__(self, username, title, pw_hash):
		self.username = username
		self.title = title
		self.pw_hash = pw_hash

	def __repr__(self):
		return '<User {}>'.format(self.username)
class Event(db.Model):
		event_id = db.Column(db.Integer, primary_key=True)
		date = db.Column(db.Date, nullable =False)
		booked_by_user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
		
		
		def __init__(self, date, booked_by_user_id):
			self.date = date
			self.booked_by_user_id = booked_by_user_id
		
		def __repr__ (self):
			return '<Events {}'.format(self.event_id)


class Event_Assignee(db.Model):
		event_assignee_id = db.Column(db.Integer, primary_key=True)
		event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'), nullable=False)
		user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
		
		def __init__(self, event_id, user_id):
			self.event_id = event_id;
			self.user_id = user_id
			
		def __repr__(self):
			return 'Event Assignee {}'.format(self.event_assignee_id)
		
# 
# class Message(db.Model):
# 	message_id = db.Column(db.Integer, primary_key=True)
# 	author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
# 	text = db.Column(db.Text, nullable=False)
# 	pub_date = db.Column(db.Integer)
# 
# 	def __init__(self, author_id, text, pub_date):
# 			self.author_id = author_id
# 			self.text = text
# 			self.pub_date = pub_date
# 
# 	def __repr__(self):
# 			return '<Message {}'.format(self.message_id)
