#-*-coding:utf-8-*-
from flask import render_template, flash, redirect, session, url_for, request, g, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from .forms import *
from .models import *
from copy import deepcopy
import os, json

@app.before_request
def before_request():
	g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm(prefix='login-')
	if form.validate_on_submit():
		flash(u'登录成功')
		u = User.query.filter_by(username=form.username.data).first()
		login_user(u)
		return redirect('/')
	return render_template('login.html', form=form)

@app.route('/register/', methods = ['POST', 'GET'])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		user = User()
		form.populate_obj(user)
		db.session.add(user)
		db.session.commit()
		flash(u'注册成功')
		login_user(user)
		return redirect(url_for('index'))
	return render_template('register.html', form=form)

@app.route('/logout')
def logout():
	session.clear()
	logout_user()
	return redirect('/')

@app.route('/')
def index():
	return redirect(url_for('view_summary_list'))

@app.route('/about')
def show_about():
	return render_template('about.html')

@app.route('/view_members')
def view_members():
	items = Member.query.all()
	return render_template('view_members.html', members = items)

@login_required
@app.route('/edit_member', methods = ['POST', 'GET'])
@app.route('/edit_member/<int:id>', methods = ['POST', 'GET'])
def edit_member(id=0):
	item = Member() if id == 0 else Member.query.get_or_404(id)
	form = AddMemberForm(obj = item)
	if form.validate_on_submit():
		form.populate_obj(item)
		db.session.add(item)
		db.session.commit()
		return redirect(url_for('view_members'))
	return render_template('edit_member.html', form=form, mid = id)

@app.route('/view_summary_list')
def view_summary_list():
	items = ContestSummary.query.all()
	return render_template('view_summary_list.html', summary = items)

@login_required
@app.route('/edit_summary/', methods=['POST', 'GET'])
@app.route('/edit_summary/<int:id>', methods=['POST', 'GET'])
def edit_summary_info(id=0):
	item = ContestSummary() if id == 0 else ContestSummary.query.get_or_404(id)
	items = TeamSummary.query.filter(TeamSummary.contest_id == id).all()
	form = ContestSummaryForm(obj = item)
	if form.validate_on_submit():
		form.populate_obj(item)
		db.session.add(item)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('edit_contest_summary.html', form=form, cid = id, teams = items)

@app.route('/view_summary/<int:id>')
def view_contest_summary(id):
	item = ContestSummary.query.get_or_404(id)
	items = TeamSummary.query.filter(TeamSummary.contest_id == id).all()
	items.sort(key = lambda u:u.rank)
	board = list(map(lambda u:u.rstrip('\r').split('\t'), item.board.split('\n')))
	for x in board:
		while len(x) > item.countp + 4:
			x.pop()
	return render_template('view_contest_summary.html',
		contest_summary = item,
		team_summary = items,
		board = board)

@app.route('/edit_team_summary/<int:cid>/', methods=['POST', 'GET'])
@app.route('/edit_team_summary/<int:cid>/id/<int:id>', methods=['POST', 'GET'])
@login_required
def edit_team_summary(cid, id=0):
	item = TeamSummary() if id == 0 else TeamSummary.query.get_or_404(id)
	contest = ContestSummary.query.get_or_404(cid)
	form = TeamInfoForm(countp = contest.countp, obj = item)
	if form.validate_on_submit():
		form.populate_obj(item)
		item.contest_id = cid
		item.acinfo = form.acinfo
		db.session.add(item)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('edit_team_summary.html', form=form, cid = cid, tid = id, countp = contest.countp)

@app.route('/delete_team_summary/<int:cid>/id/<int:id>')
@login_required
def delete_team_summary(cid, id):
	item = TeamSummary.query.get_or_404(id)
	try:
		db.session.delete(item)
		db.session.commit()
	except:
		flash(u'队伍删除失败', category='error')
	return redirect(url_for('edit_summary_info', id = cid))

@app.route('/delete_contest_summary/<int:cid>')
@login_required
def delete_contest_summary(cid):
	item = ContestSummary.query.get_or_404(cid)
	try:
		db.session.delete(item)
		db.session.commit()
	except:
		flash(u'比赛删除失败', category='error')
	return redirect(url_for('index'))

@app.route('/rate', defaults = {'begin': 27, 'end': len(ContestSummary.query.filter().all())})
@app.route('/rate/<int:begin>/<int:end>')
@login_required
def rate_summary(begin, end):
	return render_template('rate.html',
		data = get_rate_data(begin, end),
		slider = {
			'min': 0,
			'max': len(ContestSummary.query.filter().all()),
			'left': begin,
			'right': end
		}
	)

@app.route('/rate_data/<int:begin>/<int:end>')
@login_required
def get_rate_data(begin, end):
	items = TeamSummary.query.filter().all()
	contest_items = ContestSummary.query.filter().all()
	contests = sorted(list(map(lambda u: (u.date, u.id), contest_items)))
	contests = list(map(lambda u: u[1], contests))[begin:end]
	contest_name = dict(map(lambda u: (u.id, u.name), contest_items))
	logs = dict(map(lambda c: (c, sorted(map(lambda u: [u.rank, u.team_name], filter(lambda u: u.contest_id == c, items)))), contests))
	teamnames = sorted(list(set(map(lambda u: u.team_name.replace('Team', 'team').replace('kir', 'team1'), items))))

	history_rate = dict(map(lambda name: (name, [['Initial', 1500.0]]), teamnames))
	rate = dict(map(lambda name: (name, 1500.0), teamnames))
	K = 16
	for c in contests:
		new_rate = deepcopy(rate)
		n = len(logs[c])
		for i in range(n):
			for j in range(n):
				if i >= j:
					continue
				a = logs[c][i][1].replace('Team', 'team').replace('kir', 'team1')
				b = logs[c][j][1].replace('Team', 'team').replace('kir', 'team1')
				q_a = 10 ** (rate[a] / 400)
				q_b = 10 ** (rate[b] / 400)
				e_a = q_a / (q_a + q_b)
				e_b = q_b / (q_a + q_b)
				new_rate[a] = new_rate[a] + K * (1 - e_a)
				new_rate[b] = new_rate[b] + K * (0 - e_b)
		rate = deepcopy(new_rate)
		for name in teamnames:
			history_rate[name].append([contest_name[c], rate[name]])

	res = []
	hue = 0
	for name in teamnames:
		hr = history_rate[name]
		res.append({
			'label': name,
			'fill': False,
			'borderColor': 'hsl(%d, 100%%, 50%%)' % hue,
			'data': list(map(lambda u: {
				'x': u[0],
				'y': u[1][1],
				'n': u[1][0]
			}, enumerate(hr)))
		})
		hue += 360 / len(teamnames)

	return json.dumps(res)

@app.route('/count/<username>')
def count(username):
	from app.oj import get_all
	return render_template('count.html', username = username, data = get_all(username))
