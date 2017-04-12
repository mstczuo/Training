import requests, re

def get(username):
	url = 'http://poj.org/userstatus?user_id=%s' % username
	s = requests.get(url)
	r = re.findall(r'status.+?>(\d+)', s.text)

	try:
		return {'solved': int(r[0]), 'attempts': int(r[1])}
	except IndexError:
		return {'error': 'user not found'}
