import requests, re

def get(username):
	url = 'http://acm.zju.edu.cn/onlinejudge/showRuns.do?contestId=1&handle=%s' % username
	s = requests.get(url)
	r = re.findall(r'userId=(\d+)', s.text)
	try:
		uid = r[0]
	except IndexError:
		return {'error': 'user not found'}
	url = 'http://acm.zju.edu.cn/onlinejudge/showUserStatus.do?userId=%s' % uid
	s = requests.get(url)
	r = re.findall(r'size="4">(\d+)/(\d+)', s.text)[0]
	return {'solved': int(r[0]), 'attempts': int(r[1])}
