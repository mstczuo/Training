#-*-coding:utf-8-*-
from flask_wtf import Form
from flask import request
from wtforms import StringField, BooleanField, ValidationError
from wtforms.validators import *
from wtforms.fields import *
from wtforms.widgets import *
from .models import *

class LoginForm(Form):
	username = TextField(u'登陆名', validators = [Required(message = u'登录名是必填项')])
	password = PasswordField(u'密码', validators = [Required(message = u'密码是必填项')])
	submit = SubmitField(u'登陆')

	def validate_password(self, field):
		u = User.query.filter_by(username=self.username.data).first()
		if u is None or not u.verify_password(field.data):
			raise ValidationError(u'用户名或密码错误')

class PostForm(Form):
	title = TextField(u'标题', validators = [Required(message = u'标题是必填项')])
	author = TextField(u'发布者', validators = [Required(message = u'发布者是必填项')])
	content = TextAreaField(u'正文', validators = [Required(message = u'正文是必填项')])
	submit = SubmitField(u'提交')

def get_choices(itemlist, empty_name = u'空'):
	return [(0, empty_name)] + [(item.id, item.name) for item in itemlist]

class RegisterForm(Form):
	username = TextField(u'登录名', validators = [Required()])
	password = TextField(u'密码', validators = [Required()])
	confirm = TextField(u'确认密码', validators = [Required(), EqualTo('password', message=u'密码不匹配')])
	submit = SubmitField(u'注册')

	def validate_username(self, filed):
		u = User.query.filter(User.username == filed.data).first()
		if u is not None:
			raise ValidationError(u'用户早已存在')

class AddMemberForm(Form):
	name = TextField(u'队员姓名')
	grade = TextField(u'年级')
	major = TextField(u'专业')
	submit = SubmitField(u'添加')

class ContestSummaryForm(Form):
	name = TextField(u'比赛名称', validators = [Required()])
	source = TextField(u'比赛来源', validators = [Required()])
	board = TextAreaField(u'Board', validators = [Required()])
	date = DateTimeField(u'日期')
	countp = SelectField(u'题数', coerce = int, choices = [(cnt, '%d - %c' % (cnt, chr(64 + cnt))) for cnt in range(5, 14)])
	submit = SubmitField(u'提交')

class TeamInfoForm(Form):
	team_name = TextField(u'队伍名称', validators = [Required()])
	rank = TextField(u'排名', validators = [Required()])
	team_member1 = SelectField(u'队员A', coerce = int, choices = [])
	team_member2 = SelectField(u'队员B', coerce = int, choices = [])
	team_member3 = SelectField(u'队员C', coerce = int, choices = [])
	
	A = FieldList(BooleanField(u''), label='队员A', min_entries=5)
	B = FieldList(BooleanField(u''), label='队员B', min_entries=5)
	C = FieldList(BooleanField(u''), label='队员C', min_entries=5)
	AC = FieldList(BooleanField(u''), label='AC', min_entries=5)
	NA = FieldList(BooleanField(u'', default=True), label='未AC', min_entries=5)
	SC = FieldList(BooleanField(u''), label='赛后AC', min_entries=5)
	
	submit = SubmitField(u'提交')

	def __init__(self, countp, obj = None, **kwards):
		Form.__init__(self, obj = obj, **kwards)
		items = get_choices(Member.query.all(), u'请选择队员')
		self.team_member1.choices = items
		self.team_member2.choices = items
		self.team_member3.choices = items
		for i in range(countp - 5):
			self.A._add_entry()
			self.B._add_entry()
			self.C._add_entry()
			self.AC._add_entry()
			self.NA._add_entry()
			self.SC._add_entry()
		if self.is_submitted():
			formdata = dict(request.form)
			for i in range(countp):
				self.A.entries[i].data = formdata.has_key('A-%d' % i)
				self.B.entries[i].data = formdata.has_key('B-%d' % i)
				self.C.entries[i].data = formdata.has_key('C-%d' % i)
				self.AC.entries[i].data = formdata.has_key('AC-%d' % i)
				self.NA.entries[i].data = formdata.has_key('NA-%d' % i)
				self.SC.entries[i].data = formdata.has_key('SC-%d' % i)
		else:
			if obj is not None:
				self.set_acinfo(obj.acinfo)

	def validate_rank(self, field):
		_rank = 0
		try:
			_rank = int(field.data)
		except:
			raise ValidationError(u'排名需要是整数')
		if _rank <= 0:
			raise ValidationError(u'排名必须大于零')
	
	@property
	def acinfo(self):
		return str([self.A.data, self.B.data, self.C.data, self.AC.data, self.NA.data, self.SC.data])

	def set_acinfo(self, value):
		if value is None: return
		countp = len(self.A.entries)
		value = eval(value)
		for i in range(countp):
			self.A.entries[i].data = value[0][i]
			self.B.entries[i].data = value[1][i]
			self.C.entries[i].data = value[2][i]
			self.AC.entries[i].data = value[3][i]
			self.NA.entries[i].data = value[4][i]
			self.SC.entries[i].data = value[5][i]
