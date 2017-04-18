## Automated problem counter

This folder contains scripts to count problems from many different online judges with username.

### How to add a new one

> Say we are adding scripts for soj

1. __Write script__

	Create python code under this folder, such as `soj.py` (Full path: `/app/oj/soj.py`)

	The script should looked like this:
	```python
	import modules_you_need

	def get(username):
		try:
			# Codes to get data from the online judge, such as
			solved = get_solved_from_oj()
			attempts = get_attempts_from_oj()
		except:
			# Deal with error
			return {'error': 'details of error'}
		else:
			return {'solved': solved, 'attempts': attempts}
	```
	If you are still confusing, reading existing `poj.py` will be a good choice.

2. __Add to list__

	Open `oj_list.py` under this folder (`/app/oj/oj_list.py`)

	Add your file to `oj_list`. Change
	```python
	oj_list = ['poj', 'zoj']
	```
	To
	```python
	oj_list = ['poj', 'zoj', 'soj']
	```

That's all. Run the script or reload your webserver, access `/count/username`, everything should work like a charm.
