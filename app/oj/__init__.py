from importlib import import_module
from .oj_list import oj_list

for oj in oj_list:
	import_module('.%s' % oj, __package__)
