#-*- coding:utf-8 -*-
from app import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin

class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(256))
	author = db.Column(db.String(256))
	content = db.Column(db.Text)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20))
	password = db.Column(db.String(80))

	def verify_password(self, data):
		return self.password == data

class Member(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(20))
	grade = db.Column(db.Integer)
	major = db.Column(db.String(20))

class ContestSummary(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(40))
	source = db.Column(db.String(40))
	board = db.Column(db.Text)
	countp = db.Column(db.Integer)
	date = db.Column(db.DateTime)

class TeamSummary(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	team_name = db.Column(db.String(40))
	contest_id = db.Column(db.Integer, db.ForeignKey('contest_summary.id'))
	rank = db.Column(db.Integer)
	team_member1 = db.Column(db.Integer, db.ForeignKey('member.id'))
	team_member2 = db.Column(db.Integer, db.ForeignKey('member.id'))
	team_member3 = db.Column(db.Integer, db.ForeignKey('member.id'))
	member1 = db.relationship("Member", foreign_keys = team_member1)
	member2 = db.relationship("Member", foreign_keys = team_member2)
	member3 = db.relationship("Member", foreign_keys = team_member3)
	acinfo = db.Column(db.String(240))

class AnonymousUser(AnonymousUserMixin):
	pass

@login_manager.user_loader
def load_user(id):
	return User.query.get(id)

