from importlib import import_module

oj_list = ['poj', 'zju']

for oj in oj_list:
	import_module('.%s' % oj, __package__)

def get_all(username):
	res = {'total': {'solved': 0, 'attempts': 0}}
	for oj in oj_list:
		res[oj] = eval('%s.get("%s")' % (oj, username))
		try:
			res['total']['solved'] += res[oj]['solved']
			res['total']['attempts'] += res[oj]['attempts']
		except KeyError:
			pass
	return res
