import requests, re

def get(username):
    url = 'https://vjudge.net/user/%s' % username
    s = requests.get(url)
    r = re.findall('blank">(\d+)', s.text)
    try:
        return {'solved': int(r[3]), 'attempts': int(r[4])}
    except IndexError:
        return {'error': 'user not found'}
